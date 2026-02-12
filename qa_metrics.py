#!/usr/bin/env python3
"""
LockN Score QA - Reliability Metrics Analysis Framework

Analyzes pipeline output JSON files to compute per-clip and aggregate metrics
for ball detection, audio events, score accuracy, and latency.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Any

import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt


def load_pipeline_output(filepath: str) -> list[dict[str, Any]]:
    """Load pipeline output JSON file containing per-clip results."""
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    # Support both single clip and list of clips
    if isinstance(data, dict):
        return [data]
    return data


def compute_detection_metrics(detected_frames: list[int], 
                              ground_truth_frames: list[int],
                              total_frames: int) -> dict[str, float]:
    """
    Compute ball detection metrics: precision, recall, F1.
    
    Args:
        detected_frames: List of frame indices where ball was detected
        ground_truth_frames: List of frame indices where ball actually appears
        total_frames: Total number of frames in the clip
    
    Returns:
        Dictionary with precision, recall, F1, TP, FP, FN counts
    """
    detected_set = set(detected_frames)
    gt_set = set(ground_truth_frames)
    
    true_positives = len(detected_set & gt_set)
    false_positives = len(detected_set - gt_set)
    false_negatives = len(gt_set - detected_set)
    
    precision = true_positives / len(detected_set) if detected_set else 0.0
    recall = true_positives / len(gt_set) if gt_set else 0.0
    
    if precision + recall > 0:
        f1 = 2 * precision * recall / (precision + recall)
    else:
        f1 = 0.0
    
    return {
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'true_positives': true_positives,
        'false_positives': false_positives,
        'false_negatives': false_negatives,
        'total_detected': len(detected_set),
        'total_ground_truth': len(gt_set),
        'coverage': len(gt_set) / total_frames if total_frames > 0 else 0.0
    }


def compute_audio_metrics(detected_events: list[dict[str, Any]],
                          ground_truth_events: list[dict[str, Any]]) -> dict[str, float]:
    """
    Compute audio event detection metrics: TPR, FPR.
    
    Args:
        detected_events: List of detected audio events with 'frame' and 'type'
        ground_truth_events: List of ground truth audio events with 'frame' and 'type'
    
    Returns:
        Dictionary with true_positive_rate, false_positive_rate, precision, recall
    """
    # Define matching tolerance (frames)
    tolerance = 5
    
    def matches(detected: dict, gt: dict) -> bool:
        """Check if detected event matches ground truth within tolerance."""
        if detected.get('type') != gt.get('type'):
            return False
        return abs(detected.get('frame', 0) - gt.get('frame', 0)) <= tolerance
    
    true_positives = 0
    detected_matched = set()
    gt_matched = set()
    
    for i, det in enumerate(detected_events):
        for j, gt in enumerate(ground_truth_events):
            if i not in detected_matched and j not in gt_matched and matches(det, gt):
                true_positives += 1
                detected_matched.add(i)
                gt_matched.add(j)
                break
    
    false_positives = len(detected_events) - true_positives
    false_negatives = len(ground_truth_events) - true_positives
    
    true_positive_rate = true_positives / len(ground_truth_events) if ground_truth_events else 0.0
    false_positive_rate = false_positives / max(len(detected_events), 1)
    
    precision = true_positives / len(detected_events) if detected_events else 0.0
    recall = true_positives / len(ground_truth_events) if ground_truth_events else 0.0
    
    return {
        'true_positive_rate': true_positive_rate,
        'false_positive_rate': false_positive_rate,
        'precision': precision,
        'recall': recall,
        'true_positives': true_positives,
        'false_positives': false_positives,
        'false_negatives': false_negatives,
        'total_detected_events': len(detected_events),
        'total_ground_truth_events': len(ground_truth_events)
    }


def compute_score_accuracy(predicted_score: float, ground_truth_score: float) -> dict[str, float]:
    """
    Compute score accuracy metrics.
    
    Args:
        predicted_score: Predicted score from pipeline
        ground_truth_score: Ground truth score
    
    Returns:
        Dictionary with absolute_error, relative_error, error_percent
    """
    absolute_error = abs(predicted_score - ground_truth_score)
    relative_error = absolute_error / abs(ground_truth_score) if ground_truth_score != 0 else 0.0
    error_percent = relative_error * 100
    
    return {
        'absolute_error': absolute_error,
        'relative_error': relative_error,
        'error_percent': error_percent,
        'predicted_score': predicted_score,
        'ground_truth_score': ground_truth_score,
        'score_difference': predicted_score - ground_truth_score
    }


def compute_latency_metrics(processing_times: list[float]) -> dict[str, float]:
    """
    Compute latency metrics: p50, p95, p99.
    
    Args:
        processing_times: List of frame processing times in milliseconds
    
    Returns:
        Dictionary with latency percentiles and statistics
    """
    if not processing_times:
        return {
            'p50': 0.0, 'p95': 0.0, 'p99': 0.0,
            'min': 0.0, 'max': 0.0, 'mean': 0.0, 'std': 0.0
        }
    
    return {
        'p50': float(np.percentile(processing_times, 50)),
        'p95': float(np.percentile(processing_times, 95)),
        'p99': float(np.percentile(processing_times, 99)),
        'min': float(min(processing_times)),
        'max': float(max(processing_times)),
        'mean': float(np.mean(processing_times)),
        'std': float(np.std(processing_times))
    }


def analyze_clip(clip_data: dict[str, Any]) -> dict[str, Any]:
    """
    Analyze a single clip and compute all metrics.
    
    Args:
        clip_data: Dictionary containing clip results from pipeline
    
    Returns:
        Dictionary with all computed metrics for this clip
    """
    clip_id = clip_data.get('clip_id', clip_data.get('id', 'unknown'))
    
    # Extract data from clip
    ball_detection = clip_data.get('ball_detection', {})
    audio_events = clip_data.get('audio_events', {})
    score = clip_data.get('score', {})
    latency = clip_data.get('latency', {})
    
    # Compute metrics
    detection_metrics = compute_detection_metrics(
        detected_frames=ball_detection.get('detected_frames', []),
        ground_truth_frames=ball_detection.get('ground_truth_frames', []),
        total_frames=ball_detection.get('total_frames', 0)
    )
    
    audio_metrics = compute_audio_metrics(
        detected_events=audio_events.get('detected_events', []),
        ground_truth_events=audio_events.get('ground_truth_events', [])
    )
    
    score_metrics = compute_score_accuracy(
        predicted_score=score.get('predicted', 0),
        ground_truth_score=score.get('ground_truth', 0)
    )
    
    latency_metrics = compute_latency_metrics(
        processing_times=latency.get('processing_times_ms', [])
    )
    
    return {
        'clip_id': clip_id,
        'detection_metrics': detection_metrics,
        'audio_metrics': audio_metrics,
        'score_metrics': score_metrics,
        'latency_metrics': latency_metrics
    }


def bootstrap_confidence_interval(data: list[float], 
                                  stat_func=np.mean, 
                                  n_bootstrap: int = 1000, 
                                  confidence: float = 0.95) -> dict[str, float]:
    """
    Compute bootstrap confidence interval for a statistic.
    
    Args:
        data: Sample data
        stat_func: Function to compute statistic (default: mean)
        n_bootstrap: Number of bootstrap samples
        confidence: Confidence level (default: 0.95)
    
    Returns:
        Dictionary with point_estimate, ci_lower, ci_upper
    """
    if len(data) < 2:
        return {
            'point_estimate': float(stat_func(data)) if data else 0.0,
            'ci_lower': 0.0,
            'ci_upper': 0.0,
            'ci_width': 0.0
        }
    
    bootstrap_samples = []
    for _ in range(n_bootstrap):
        sample = np.random.choice(data, size=len(data), replace=True)
        bootstrap_samples.append(stat_func(sample))
    
    bootstrap_samples = np.array(bootstrap_samples)
    point_estimate = stat_func(data)
    
    alpha = 1 - confidence
    ci_lower = float(np.percentile(bootstrap_samples, 100 * alpha / 2))
    ci_upper = float(np.percentile(bootstrap_samples, 100 * (1 - alpha / 2)))
    
    return {
        'point_estimate': float(point_estimate),
        'ci_lower': float(ci_lower),
        'ci_upper': float(ci_upper),
        'ci_width': float(ci_upper - ci_lower),
        'std_error': float(np.std(bootstrap_samples))
    }


def compute_aggregate_metrics(clip_results: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Compute aggregate metrics across all clips.
    
    Args:
        clip_results: List of analyzed clip results
    
    Returns:
        Dictionary with aggregate statistics
    """
    if not clip_results:
        return {}
    
    # Extract metric values
    precisions = [c['detection_metrics']['precision'] for c in clip_results]
    recalls = [c['detection_metrics']['recall'] for c in clip_results]
    f1_scores = [c['detection_metrics']['f1'] for c in clip_results]
    
    tpr_scores = [c['audio_metrics']['true_positive_rate'] for c in clip_results]
    fpr_scores = [c['audio_metrics']['false_positive_rate'] for c in clip_results]
    
    abs_errors = [c['score_metrics']['absolute_error'] for c in clip_results]
    rel_errors = [c['score_metrics']['relative_error'] for c in clip_results]
    
    p50_latencies = [c['latency_metrics']['p50'] for c in clip_results]
    p95_latencies = [c['latency_metrics']['p95'] for c in clip_results]
    p99_latencies = [c['latency_metrics']['p99'] for c in clip_results]
    
    # Compute aggregate statistics with confidence intervals
    metrics = {
        'ball_detection': {
            'precision': bootstrap_confidence_interval(precisions),
            'recall': bootstrap_confidence_interval(recalls),
            'f1': bootstrap_confidence_interval(f1_scores)
        },
        'audio_events': {
            'true_positive_rate': bootstrap_confidence_interval(tpr_scores),
            'false_positive_rate': bootstrap_confidence_interval(fpr_scores)
        },
        'score_accuracy': {
            'absolute_error': bootstrap_confidence_interval(abs_errors),
            'relative_error': bootstrap_confidence_interval(rel_errors)
        },
        'latency': {
            'p50': bootstrap_confidence_interval(p50_latencies),
            'p95': bootstrap_confidence_interval(p95_latencies),
            'p99': bootstrap_confidence_interval(p99_latencies)
        }
    }
    
    # Add simple statistics (non-bootstrap)
    metrics['summary'] = {
        'total_clips': len(clip_results),
        'mean_precision': float(np.mean(precisions)),
        'mean_recall': float(np.mean(recalls)),
        'mean_f1': float(np.mean(f1_scores)),
        'mean_absolute_error': float(np.mean(abs_errors)),
        'mean_p50_latency': float(np.mean(p50_latencies))
    }
    
    return metrics


def classify_clip_pass_fail(clip_result: dict[str, Any], 
                            thresholds: dict[str, float] = None) -> dict[str, Any]:
    """
    Classify a clip as pass/fail based on configurable thresholds.
    
    Args:
        clip_result: Analyzed clip result
        thresholds: Dictionary of threshold values
    
    Returns:
        Dictionary with pass/fail classification and reasons
    """
    if thresholds is None:
        thresholds = {
            'min_precision': 0.8,
            'min_recall': 0.7,
            'min_f1': 0.75,
            'max_abs_error': 10.0,
            'min_tpr': 0.95,  # Lower bound for TPR
            'max_fpr': 0.1,   # Upper bound for FPR
            'max_p99_latency_ms': 100.0
        }
    
    issues = []
    passed = True
    
    detection = clip_result['detection_metrics']
    if detection['precision'] < thresholds['min_precision']:
        issues.append(f"Precision {detection['precision']:.3f} < {thresholds['min_precision']}")
        passed = False
    if detection['recall'] < thresholds['min_recall']:
        issues.append(f"Recall {detection['recall']:.3f} < {thresholds['min_recall']}")
        passed = False
    if detection['f1'] < thresholds['min_f1']:
        issues.append(f"F1 {detection['f1']:.3f} < {thresholds['min_f1']}")
        passed = False
    
    score = clip_result['score_metrics']
    if score['absolute_error'] > thresholds['max_abs_error']:
        issues.append(f"Score error {score['absolute_error']:.2f} > {thresholds['max_abs_error']}")
        passed = False
    
    audio = clip_result['audio_metrics']
    if audio['true_positive_rate'] < thresholds['min_tpr']:
        issues.append(f"TPR {audio['true_positive_rate']:.3f} < {thresholds['min_tpr']}")
        passed = False
    if audio['false_positive_rate'] > thresholds['max_fpr']:
        issues.append(f"FPR {audio['false_positive_rate']:.3f} > {thresholds['max_fpr']}")
        passed = False
    
    latency = clip_result['latency_metrics']
    if latency['p99'] > thresholds['max_p99_latency_ms']:
        issues.append(f"P99 latency {latency['p99']:.2f}ms > {thresholds['max_p99_latency_ms']}ms")
        passed = False
    
    return {
        'passed': passed,
        'clip_id': clip_result['clip_id'],
        'issues': issues,
        'score': len(issues)  # Lower is better
    }


def analyze_failure_modes(results: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Analyze and group failures by type.
    
    Args:
        results: List of classification results
    
    Returns:
        Dictionary with failure mode analysis
    """
    failure_types = {}
    clips_by_failure = {}
    
    for result in results:
        if not result['passed']:
            clip_id = result['clip_id']
            for issue in result['issues']:
                # Extract failure type from issue description
                if 'Precision' in issue:
                    ftype = 'precision'
                elif 'Recall' in issue:
                    ftype = 'recall'
                elif 'F1' in issue:
                    ftype = 'f1'
                elif 'Score error' in issue:
                    ftype = 'score_error'
                elif 'TPR' in issue:
                    ftype = 'tpr_high'
                elif 'FPR' in issue:
                    ftype = 'fpr_high'
                elif 'latency' in issue:
                    ftype = 'latency'
                else:
                    ftype = 'other'
                
                if ftype not in failure_types:
                    failure_types[ftype] = {'count': 0, 'clips': []}
                
                failure_types[ftype]['count'] += 1
                if clip_id not in failure_types[ftype]['clips']:
                    failure_types[ftype]['clips'].append(clip_id)
                
                if ftype not in clips_by_failure:
                    clips_by_failure[ftype] = []
                if clip_id not in clips_by_failure[ftype]:
                    clips_by_failure[ftype].append(clip_id)
    
    return {
        'total_failures': len([r for r in results if not r['passed']]),
        'total_passes': len([r for r in results if r['passed']]),
        'failure_rate': len([r for r in results if not r['passed']]) / max(len(results), 1),
        'failure_types': failure_types,
        'clips_by_failure': clips_by_failure
    }


def generate_recommendations(aggregate_metrics: dict[str, Any],
                            failure_analysis: dict[str, Any]) -> list[str]:
    """
    Generate actionable recommendations based on analysis.
    
    Args:
        aggregate_metrics: Computed aggregate metrics
        failure_analysis: Failure mode analysis results
    
    Returns:
        List of recommendation strings
    """
    recommendations = []
    
    # Check ball detection metrics
    ball_det = aggregate_metrics.get('ball_detection', {})
    if ball_det:
        precision = ball_det.get('precision', {})
        if precision.get('point_estimate', 1.0) < 0.9:
            recommendations.append(
                "Ball detection precision is below 90%. Consider improving the detection model "
                "or adding more training data for edge cases."
            )
        
        recall = ball_det.get('recall', {})
        if recall.get('point_estimate', 1.0) < 0.85:
            recommendations.append(
                "Ball detection recall is below 85%. Consider adjusting detection thresholds "
                "or implementing multi-frame tracking to reduce missed detections."
            )
    
    # Check audio metrics
    audio = aggregate_metrics.get('audio_events', {})
    if audio:
        fpr = audio.get('false_positive_rate', {})
        if fpr.get('point_estimate', 0.0) > 0.05:
            recommendations.append(
                "Audio event false positive rate is high (>5%). Consider implementing "
                "temporal smoothing or additional audio feature filtering."
            )
    
    # Check score accuracy
    score_acc = aggregate_metrics.get('score_accuracy', {})
    if score_acc:
        abs_err = score_acc.get('absolute_error', {})
        if abs_err.get('point_estimate', 0.0) > 5.0:
            recommendations.append(
                "Score prediction error is high. Consider refining the scoring algorithm "
                "or adding more ground truth data for calibration."
            )
    
    # Check latency
    latency = aggregate_metrics.get('latency', {})
    if latency:
        p99 = latency.get('p99', {})
        if p99.get('point_estimate', 0.0) > 50.0:
            recommendations.append(
                "P99 latency exceeds 50ms. Consider optimizing the processing pipeline, "
                "implementing frame skipping for slow clips, or using hardware acceleration."
            )
    
    # Check failure modes
    failure_types = failure_analysis.get('failure_types', {})
    if 'latency' in failure_types:
        recommendations.append(
            "Latency issues detected in multiple clips. Consider profiling the pipeline "
            "to identify bottlenecks and implement caching where appropriate."
        )
    
    if 'fpr_high' in failure_types:
        recommendations.append(
            "High false positive rate in audio detection. Consider implementing "
            "context-aware filtering or additional validation layers."
        )
    
    # General recommendations
    if failure_analysis.get('total_failures', 0) > 0:
        recommendations.append(
            f"Overall failure rate: {failure_analysis.get('failure_rate', 0):.1%}. "
            "Prioritize clips with repeated failures for targeted improvement."
        )
    
    return recommendations


def generate_markdown_report(clip_results: list[dict[str, Any]],
                            aggregate_metrics: dict[str, Any],
                            classification_results: list[dict[str, Any]],
                            failure_analysis: dict[str, Any],
                            recommendations: list[str],
                            output_path: str = 'qa_report.md') -> str:
    """
    Generate a markdown report with all analysis results.
    
    Args:
        clip_results: List of analyzed clip results
        aggregate_metrics: Computed aggregate metrics
        classification_results: Pass/fail classification results
        failure_analysis: Failure mode analysis
        recommendations: Generated recommendations
        output_path: Path to save the report
    
    Returns:
        Path to the generated report
    """
    report = []
    
    # Header
    report.append("# LockN Score QA - Reliability Report\n")
    report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report.append(f"**Total Clips Analyzed:** {len(clip_results)}\n")
    
    # Summary Section
    report.append("\n## Summary\n")
    report.append("| Metric | Point Estimate | 95% CI Lower | 95% CI Upper |")
    report.append("|--------|----------------|--------------|--------------|")
    
    ball_det = aggregate_metrics.get('ball_detection', {})
    if ball_det:
        report.append(f"| Ball Detection Precision | {ball_det['precision']['point_estimate']:.4f} | "
                     f"{ball_det['precision']['ci_lower']:.4f} | {ball_det['precision']['ci_upper']:.4f} |")
        report.append(f"| Ball Detection Recall | {ball_det['recall']['point_estimate']:.4f} | "
                     f"{ball_det['recall']['ci_lower']:.4f} | {ball_det['recall']['ci_upper']:.4f} |")
        report.append(f"| Ball Detection F1 | {ball_det['f1']['point_estimate']:.4f} | "
                     f"{ball_det['f1']['ci_lower']:.4f} | {ball_det['f1']['ci_upper']:.4f} |")
    
    audio = aggregate_metrics.get('audio_events', {})
    if audio:
        report.append(f"| Audio TPR | {audio['true_positive_rate']['point_estimate']:.4f} | "
                     f"{audio['true_positive_rate']['ci_lower']:.4f} | {audio['true_positive_rate']['ci_upper']:.4f} |")
        report.append(f"| Audio FPR | {audio['false_positive_rate']['point_estimate']:.4f} | "
                     f"{audio['false_positive_rate']['ci_lower']:.4f} | {audio['false_positive_rate']['ci_upper']:.4f} |")
    
    score_acc = aggregate_metrics.get('score_accuracy', {})
    if score_acc:
        report.append(f"| Score Absolute Error | {score_acc['absolute_error']['point_estimate']:.4f} | "
                     f"{score_acc['absolute_error']['ci_lower']:.4f} | {score_acc['absolute_error']['ci_upper']:.4f} |")
    
    latency = aggregate_metrics.get('latency', {})
    if latency:
        report.append(f"| Latency P50 | {latency['p50']['point_estimate']:.2f} ms | "
                     f"{latency['p50']['ci_lower']:.2f} ms | {latency['p50']['ci_upper']:.2f} ms |")
        report.append(f"| Latency P95 | {latency['p95']['point_estimate']:.2f} ms | "
                     f"{latency['p95']['ci_lower']:.2f} ms | {latency['p95']['ci_upper']:.2f} ms |")
        report.append(f"| Latency P99 | {latency['p99']['point_estimate']:.2f} ms | "
                     f"{latency['p99']['ci_lower']:.2f} ms | {latency['p99']['ci_upper']:.2f} ms |")
    
    # Pass/Fail Summary
    total_pass = len([r for r in classification_results if r['passed']])
    total_fail = len([r for r in classification_results if not r['passed']])
    report.append(f"\n### Pass/Fail Summary\n")
    report.append(f"- **Passed:** {total_pass} ({total_pass/len(classification_results)*100:.1f}%)")
    report.append(f"- **Failed:** {total_fail} ({total_fail/len(classification_results)*100:.1f}%)\n")
    
    # Per-Clip Breakdown
    report.append("\n## Per-Clip Breakdown\n")
    report.append("| Clip ID | Precision | Recall | F1 | Score Error | P99 Latency | Status |")
    report.append("|---------|-----------|--------|----|-------------|-------------|--------|")
    
    for result in clip_results:
        clip_id = result['clip_id']
        det = result['detection_metrics']
        score_err = result['score_metrics']['absolute_error']
        lat = result['latency_metrics']['p99']
        
        classification = next((c for c in classification_results if c['clip_id'] == clip_id), None)
        status = "✅ Pass" if classification and classification['passed'] else "❌ Fail"
        
        report.append(f"| {clip_id} | {det['precision']:.3f} | {det['recall']:.3f} | "
                     f"{det['f1']:.3f} | {score_err:.2f} | {lat:.2f}ms | {status} |")
    
    # Failure Mode Analysis
    report.append("\n## Failure Mode Analysis\n")
    report.append(f"**Total Failures:** {failure_analysis['total_failures']}\n")
    
    if failure_analysis['failure_types']:
        report.append("### Failure Type Distribution\n")
        report.append("| Failure Type | Count | Affected Clips |")
        report.append("|--------------|-------|----------------|")
        
        for ftype, data in sorted(failure_analysis['failure_types'].items(), 
                                 key=lambda x: x[1]['count'], reverse=True):
            clips_str = ', '.join(data['clips'][:5])
            if len(data['clips']) > 5:
                clips_str += f" (+{len(data['clips']) - 5} more)"
            report.append(f"| {ftype.replace('_', ' ').title()} | {data['count']} | {clips_str} |")
    
    # Recommendations
    report.append("\n## Recommendations\n")
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            report.append(f"{i}. {rec}")
    else:
        report.append("No specific recommendations. All metrics are within acceptable ranges.")
    
    # Save report
    with open(output_path, 'w') as f:
        f.write('\n'.join(report))
    
    return output_path


def generate_plots(clip_results: list[dict[str, Any]],
                  aggregate_metrics: dict[str, Any],
                  output_dir: str = '.') -> list[str]:
    """
    Generate visualization plots for the analysis.
    
    Args:
        clip_results: List of analyzed clip results
        aggregate_metrics: Computed aggregate metrics
        output_dir: Directory to save plots
    
    Returns:
        List of paths to generated plot files
    """
    plot_paths = []
    
    # Extract data for plotting
    precisions = [r['detection_metrics']['precision'] for r in clip_results]
    recalls = [r['detection_metrics']['recall'] for r in clip_results]
    f1_scores = [r['detection_metrics']['f1'] for r in clip_results]
    abs_errors = [r['score_metrics']['absolute_error'] for r in clip_results]
    p99_latencies = [r['latency_metrics']['p99'] for r in clip_results]
    
    clip_ids = [r['clip_id'] for r in clip_results]
    
    # 1. Detection Metrics Bar Chart
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('LockN Score QA - Detection Metrics', fontsize=14, fontweight='bold')
    
    # Precision
    axes[0, 0].bar(clip_ids, precisions, color='steelblue')
    axes[0, 0].set_title('Ball Detection Precision')
    axes[0, 0].set_ylabel('Precision')
    axes[0, 0].tick_params(axis='x', rotation=45)
    axes[0, 0].axhline(y=0.8, color='green', linestyle='--', label='Target (0.8)')
    axes[0, 0].legend()
    
    # Recall
    axes[0, 1].bar(clip_ids, recalls, color='coral')
    axes[0, 1].set_title('Ball Detection Recall')
    axes[0, 1].set_ylabel('Recall')
    axes[0, 1].tick_params(axis='x', rotation=45)
    axes[0, 1].axhline(y=0.7, color='green', linestyle='--', label='Target (0.7)')
    axes[0, 1].legend()
    
    # F1 Score
    axes[1, 0].bar(clip_ids, f1_scores, color='forestgreen')
    axes[1, 0].set_title('F1 Score')
    axes[1, 0].set_ylabel('F1 Score')
    axes[1, 0].tick_params(axis='x', rotation=45)
    axes[1, 0].axhline(y=0.75, color='green', linestyle='--', label='Target (0.75)')
    axes[1, 0].legend()
    
    # Precision-Recall scatter
    axes[1, 1].scatter(precisions, recalls, s=100, alpha=0.6, color='purple')
    axes[1, 1].set_title('Precision vs Recall')
    axes[1, 1].set_xlabel('Precision')
    axes[1, 1].set_ylabel('Recall')
    axes[1, 1].axhline(y=0.7, color='gray', linestyle='--', alpha=0.5)
    axes[1, 1].axvline(x=0.8, color='gray', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plot_path = os.path.join(output_dir, 'detection_metrics.png')
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    plt.close()
    plot_paths.append(plot_path)
    
    # 2. Score and Latency Analysis
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('LockN Score QA - Score Accuracy & Latency', fontsize=14, fontweight='bold')
    
    # Score Error
    axes[0].bar(clip_ids, abs_errors, color='lightcoral')
    axes[0].set_title('Score Absolute Error')
    axes[0].set_ylabel('Absolute Error')
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].axhline(y=5.0, color='green', linestyle='--', label='Target (≤5)')
    axes[0].legend()
    
    # Latency box plot
    latency_data = [[r['latency_metrics']['p50'] for r in clip_results],
                   [r['latency_metrics']['p95'] for r in clip_results],
                   [r['latency_metrics']['p99'] for r in clip_results]]
    axes[1].boxplot(latency_data, labels=['P50', 'P95', 'P99'])
    axes[1].set_title('Processing Latency Distribution')
    axes[1].set_ylabel('Time (ms)')
    axes[1].axhline(y=50, color='green', linestyle='--', label='Target (≤50ms P99)')
    axes[1].legend()
    
    plt.tight_layout()
    plot_path = os.path.join(output_dir, 'score_latency.png')
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    plt.close()
    plot_paths.append(plot_path)
    
    # 3. Overall Metrics Summary
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('LockN Score QA - Aggregate Metrics Summary', fontsize=14, fontweight='bold')
    
    # Ball detection metrics summary
    if aggregate_metrics.get('ball_detection'):
        ball_det = aggregate_metrics['ball_detection']
        metrics_names = ['Precision', 'Recall', 'F1']
        metrics_data = [
            (ball_det['precision']['point_estimate'],
             ball_det['precision']['ci_lower'],
             ball_det['precision']['ci_upper']),
            (ball_det['recall']['point_estimate'],
             ball_det['recall']['ci_lower'],
             ball_det['recall']['ci_upper']),
            (ball_det['f1']['point_estimate'],
             ball_det['f1']['ci_lower'],
             ball_det['f1']['ci_upper'])
        ]
        
        x = np.arange(len(metrics_names))
        widths = 0.6
        
        axes[0, 0].bar(x, [m[0] for m in metrics_data], yerr=[[m[0]-m[1] for m in metrics_data], 
                      [m[2]-m[0] for m in metrics_data]], capsize=5, color='steelblue')
        axes[0, 0].set_title('Ball Detection Metrics (95% CI)')
        axes[0, 0].set_ylabel('Score')
        axes[0, 0].set_xticks(x)
        axes[0, 0].set_xticklabels(metrics_names)
        axes[0, 0].set_ylim(0, 1)
    
    # Audio metrics summary
    if aggregate_metrics.get('audio_events'):
        audio = aggregate_metrics['audio_events']
        audio_names = ['TPR', 'FPR']
        audio_data = [
            (audio['true_positive_rate']['point_estimate'],
             audio['true_positive_rate']['ci_lower'],
             audio['true_positive_rate']['ci_upper']),
            (audio['false_positive_rate']['point_estimate'],
             audio['false_positive_rate']['ci_lower'],
             audio['false_positive_rate']['ci_upper'])
        ]
        
        x = np.arange(len(audio_names))
        axes[0, 1].bar(x, [m[0] for m in audio_data], yerr=[[m[0]-m[1] for m in audio_data], 
                     [m[2]-m[0] for m in audio_data]], capsize=5, color='coral')
        axes[0, 1].set_title('Audio Event Metrics (95% CI)')
        axes[0, 1].set_ylabel('Rate')
        axes[0, 1].set_xticks(x)
        axes[0, 1].set_xticklabels(audio_names)
        axes[0, 1].set_ylim(0, 1)
    
    # Score accuracy summary
    if aggregate_metrics.get('score_accuracy'):
        score_acc = aggregate_metrics['score_accuracy']
        score_data = [
            score_acc['absolute_error']['point_estimate'],
            score_acc['relative_error']['point_estimate']
        ]
        score_names = ['Abs Error', 'Rel Error']
        
        x = np.arange(len(score_names))
        axes[1, 0].bar(x, score_data, color='forestgreen')
        axes[1, 0].set_title('Score Accuracy Metrics')
        axes[1, 0].set_ylabel('Error')
        axes[1, 0].set_xticks(x)
        axes[1, 0].set_xticklabels(score_names)
    
    # Latency summary
    if aggregate_metrics.get('latency'):
        latency = aggregate_metrics['latency']
        latency_names = ['P50', 'P95', 'P99']
        latency_data = [
            (latency['p50']['point_estimate'],
             latency['p50']['ci_lower'],
             latency['p50']['ci_upper']),
            (latency['p95']['point_estimate'],
             latency['p95']['ci_lower'],
             latency['p95']['ci_upper']),
            (latency['p99']['point_estimate'],
             latency['p99']['ci_lower'],
             latency['p99']['ci_upper'])
        ]
        
        x = np.arange(len(latency_names))
        widths = 0.6
        
        axes[1, 1].bar(x, [m[0] for m in latency_data], yerr=[[m[0]-m[1] for m in latency_data], 
                      [m[2]-m[0] for m in latency_data]], capsize=5, color='purple')
        axes[1, 1].set_title('Latency Metrics (95% CI)')
        axes[1, 1].set_ylabel('Time (ms)')
        axes[1, 1].set_xticks(x)
        axes[1, 1].set_xticklabels(latency_names)
    
    plt.tight_layout()
    plot_path = os.path.join(output_dir, 'aggregate_summary.png')
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    plt.close()
    plot_paths.append(plot_path)
    
    return plot_paths


def main():
    """Main entry point for the QA metrics analysis."""
    parser = argparse.ArgumentParser(
        description='LockN Score QA - Reliability Metrics Analysis Framework'
    )
    parser.add_argument('input_file', help='Input pipeline output JSON file')
    parser.add_argument('--output-dir', '-o', default='.', 
                       help='Output directory for report and plots (default: current)')
    parser.add_argument('--thresholds', '-t', 
                       help='Path to custom thresholds JSON file')
    parser.add_argument('--no-plots', action='store_true',
                       help='Disable plot generation')
    
    args = parser.parse_args()
    
    # Load thresholds if provided
    thresholds = None
    if args.thresholds:
        with open(args.thresholds, 'r') as f:
            thresholds = json.load(f)
    
    # Load and analyze pipeline output
    print(f"Loading pipeline output from: {args.input_file}")
    clip_data = load_pipeline_output(args.input_file)
    print(f"Found {len(clip_data)} clips to analyze")
    
    # Analyze each clip
    print("\nAnalyzing clips...")
    clip_results = [analyze_clip(clip) for clip in clip_data]
    
    # Compute aggregate metrics
    print("Computing aggregate metrics...")
    aggregate_metrics = compute_aggregate_metrics(clip_results)
    
    # Classify clips
    print("Classifying clips...")
    classification_results = [
        classify_clip_pass_fail(result, thresholds) 
        for result in clip_results
    ]
    
    # Analyze failure modes
    print("Analyzing failure modes...")
    failure_analysis = analyze_failure_modes(classification_results)
    
    # Generate recommendations
    print("Generating recommendations...")
    recommendations = generate_recommendations(aggregate_metrics, failure_analysis)
    
    # Generate report
    output_path = os.path.join(args.output_dir, 'qa_report.md')
    print(f"\nGenerating report: {output_path}")
    generate_markdown_report(clip_results, aggregate_metrics, classification_results,
                            failure_analysis, recommendations, output_path)
    
    # Generate plots if requested
    if not args.no_plots:
        print("Generating plots...")
        plot_paths = generate_plots(clip_results, aggregate_metrics, args.output_dir)
        for plot_path in plot_paths:
            print(f"  - {plot_path}")
    
    # Print summary
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)
    print(f"Total clips: {len(clip_results)}")
    print(f"Passed: {len([c for c in classification_results if c['passed']])}")
    print(f"Failed: {len([c for c in classification_results if not c['passed']])}")
    print(f"Report: {output_path}")
    print(f"Plots: {len(plot_paths) if not args.no_plots else 0} files")
    
    if recommendations:
        print(f"\nTop recommendations:")
        for rec in recommendations[:3]:
            print(f"  • {rec[:100]}...")


if __name__ == '__main__':
    main()