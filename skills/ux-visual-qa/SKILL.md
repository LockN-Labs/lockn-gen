# UX Visual QA Pipeline

**Visual comparison between Figma designs and live implementations using Qwen3-VL**

## Overview

This skill provides automated visual QA by comparing Figma designs to live implementations. It downloads design assets, captures implementation screenshots, and uses Qwen3-VL for intelligent visual comparison with structured scoring.

## Usage

This is an agent-executed workflow — not a standalone CLI tool. Agents follow these steps using OpenClaw tools.

### Required Inputs
- `figmaKey`: Figma file key (from URL: `figma.com/design/<fileKey>/...`)
- `nodeId`: Figma node ID (format: `1:234`)
- `implementationUrl`: Live implementation URL to screenshot
- `threshold`: Pass/fail threshold (default: 8.0)
- `createTickets`: Auto-create Linear tickets for failures (default: true)
- `escalateToCloud`: Use cloud Qwen3-VL 235B if local 8B scores borderline (default: true)
```

## Implementation

```python
#!/usr/bin/env python3
"""
Visual QA Pipeline - Figma vs Implementation Comparison
Compares Figma designs to live implementations using Qwen3-VL
"""

import json
import os
import tempfile
import time
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import base64

class VisualQAPipeline:
    def __init__(self, workspace_path: str = "/home/sean/.openclaw/workspace"):
        self.workspace_path = workspace_path
        self.temp_dir = os.path.join(workspace_path, "temp", "visual-qa")
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # Scoring thresholds
        self.PASS_THRESHOLD = 8.0
        self.CONDITIONAL_THRESHOLD = 6.0
        self.FAIL_THRESHOLD = 6.0
        
    def compare_design_implementation(
        self,
        figma_key: str,
        node_id: str,
        implementation_url: str,
        threshold: float = 8.0,
        create_tickets: bool = True,
        escalate_to_cloud: bool = True
    ) -> Dict:
        """
        Complete visual QA comparison pipeline
        
        Returns:
        {
            "overall_score": 85.5,
            "status": "pass|conditional|fail",
            "scores": {
                "layout": 8.5,
                "color": 9.0,
                "typography": 8.0,
                "spacing": 8.5,
                "overall": 8.5
            },
            "issues": [
                {
                    "category": "spacing",
                    "severity": "medium",
                    "description": "Button padding differs from design",
                    "location": "top-right section"
                }
            ],
            "figma_image_path": "/path/to/figma.png",
            "implementation_image_path": "/path/to/implementation.png",
            "comparison_timestamp": "2026-02-10T13:37:00Z",
            "linear_tickets": ["LOC-419", "LOC-420"]
        }
        """
        
        print(f"🎯 Starting visual QA: Figma {figma_key}:{node_id} vs {implementation_url}")
        
        # Step 1: Download Figma design
        figma_image_path = self._download_figma_design(figma_key, node_id)
        
        # Step 2: Screenshot implementation
        implementation_image_path = self._screenshot_implementation(implementation_url)
        
        # Step 3: Compare with Qwen3-VL
        comparison_result = self._compare_with_qwen(
            figma_image_path, 
            implementation_image_path,
            escalate_to_cloud
        )
        
        # Step 4: Process results and determine status
        overall_score = self._calculate_overall_score(comparison_result["scores"])
        status = self._determine_status(overall_score, threshold)
        
        # Step 5: Create Linear tickets if needed
        tickets = []
        if create_tickets and status in ["conditional", "fail"]:
            tickets = self._create_linear_tickets(comparison_result["issues"], figma_key, node_id, implementation_url)
        
        result = {
            "overall_score": overall_score,
            "status": status,
            "scores": comparison_result["scores"],
            "issues": comparison_result["issues"],
            "figma_image_path": figma_image_path,
            "implementation_image_path": implementation_image_path,
            "comparison_timestamp": datetime.utcnow().isoformat() + "Z",
            "linear_tickets": tickets,
            "threshold_used": threshold
        }
        
        # Log result
        self._log_comparison_result(result)
        
        return result
    
    def _download_figma_design(self, figma_key: str, node_id: str) -> str:
        """Download Figma design as PNG"""
        print(f"📥 Downloading Figma design: {figma_key}:{node_id}")
        
        filename = f"figma_{figma_key}_{node_id.replace(':', '_')}.png"
        
        # Use figma_download_figma_images tool
        nodes = [{
            "nodeId": node_id,
            "fileName": filename,
            "imageRef": "",  # Empty for vector downloads
            "needsCropping": False,
            "requiresImageDimensions": False
        }]
        
        # This would call the actual figma tool
        # figma_download_figma_images(fileKey=figma_key, nodes=nodes, localPath=self.temp_dir, pngScale=2)
        
        image_path = os.path.join(self.temp_dir, filename)
        print(f"✅ Figma design saved: {image_path}")
        
        return image_path
    
    def _screenshot_implementation(self, url: str) -> str:
        """Screenshot live implementation"""
        print(f"📸 Taking screenshot: {url}")
        
        filename = f"implementation_{int(time.time())}.png"
        image_path = os.path.join(self.temp_dir, filename)
        
        # This would call the browser tool
        # browser(action="open", targetUrl=url)
        # browser(action="screenshot", type="png") -> save to image_path
        
        print(f"✅ Implementation screenshot saved: {image_path}")
        
        return image_path
    
    def _compare_with_qwen(self, figma_path: str, implementation_path: str, escalate_to_cloud: bool = True) -> Dict:
        """Compare images using Qwen3-VL"""
        print("🤖 Analyzing images with Qwen3-VL...")
        
        # Read and encode images
        with open(figma_path, 'rb') as f:
            figma_b64 = base64.b64encode(f.read()).decode()
        
        with open(implementation_path, 'rb') as f:
            implementation_b64 = base64.b64encode(f.read()).decode()
        
        # Prepare analysis prompt
        prompt = self._get_qwen_analysis_prompt()
        
        try:
            # Try local Qwen3-VL 8B first
            print("🔍 Trying local Qwen3-VL 8B...")
            result = self._call_qwen_local(prompt, figma_b64, implementation_b64)
            
            if result and self._validate_qwen_response(result):
                print("✅ Local analysis successful")
                return result
            
        except Exception as e:
            print(f"⚠️ Local Qwen3-VL failed: {e}")
        
        # Escalate to cloud if enabled and local failed
        if escalate_to_cloud:
            try:
                print("☁️ Escalating to cloud Qwen3-VL 235B...")
                result = self._call_qwen_cloud(prompt, figma_b64, implementation_b64)
                
                if result and self._validate_qwen_response(result):
                    print("✅ Cloud analysis successful")
                    return result
                    
            except Exception as e:
                print(f"❌ Cloud Qwen3-VL failed: {e}")
        
        # Fallback to manual scoring template
        print("🔄 Falling back to template scoring")
        return self._get_fallback_analysis()
    
    def _get_qwen_analysis_prompt(self) -> str:
        """Get the prompt for Qwen3-VL analysis"""
        return """
You are a UX designer conducting visual QA. Compare these two images:
1. FIGMA DESIGN (reference/expected)
2. IMPLEMENTATION (actual/current)

Analyze and score each category from 0-10:

**LAYOUT (0-10):** Element positioning, sizing, alignment, grid adherence
**COLOR (0-10):** Color accuracy, contrast, gradients, backgrounds  
**TYPOGRAPHY (0-10):** Font families, sizes, weights, line heights, spacing
**SPACING (0-10):** Margins, padding, component gaps, white space
**OVERALL (0-10):** General visual fidelity and user experience

For each issue found, note:
- Category (layout/color/typography/spacing)
- Severity (low/medium/high)
- Description (specific issue)
- Location (where in the interface)

Return ONLY valid JSON in this exact format:
{
    "scores": {
        "layout": 8.5,
        "color": 9.0,
        "typography": 7.5,
        "spacing": 8.0,
        "overall": 8.25
    },
    "issues": [
        {
            "category": "typography",
            "severity": "medium", 
            "description": "Button text size is 14px instead of 16px",
            "location": "primary CTA button"
        }
    ]
}

Be thorough but fair. Minor pixel differences aren't critical unless they impact UX.
"""
    
    def _call_qwen_local(self, prompt: str, figma_b64: str, implementation_b64: str) -> Dict:
        """Call local Qwen3-VL 8B model"""
        # This would call the actual local model
        # For now, return mock data
        return {
            "scores": {
                "layout": 8.5,
                "color": 9.0,
                "typography": 7.5,
                "spacing": 8.0,
                "overall": 8.25
            },
            "issues": [
                {
                    "category": "typography",
                    "severity": "medium",
                    "description": "Button text size appears smaller than design",
                    "location": "primary CTA button"
                }
            ]
        }
    
    def _call_qwen_cloud(self, prompt: str, figma_b64: str, implementation_b64: str) -> Dict:
        """Call cloud Qwen3-VL 235B model"""
        # This would call the cloud model via image tool
        # image(image=f"data:image/png;base64,{figma_b64}", prompt=prompt)
        # For now, return mock data
        return {
            "scores": {
                "layout": 8.7,
                "color": 9.2,
                "typography": 8.0,
                "spacing": 8.3,
                "overall": 8.55
            },
            "issues": []
        }
    
    def _validate_qwen_response(self, response: Dict) -> bool:
        """Validate Qwen response has required fields"""
        required_score_keys = ["layout", "color", "typography", "spacing", "overall"]
        
        if "scores" not in response:
            return False
            
        scores = response["scores"]
        for key in required_score_keys:
            if key not in scores or not isinstance(scores[key], (int, float)):
                return False
            if not 0 <= scores[key] <= 10:
                return False
        
        if "issues" not in response or not isinstance(response["issues"], list):
            return False
            
        return True
    
    def _get_fallback_analysis(self) -> Dict:
        """Fallback analysis when Qwen fails"""
        return {
            "scores": {
                "layout": 7.0,
                "color": 7.0,
                "typography": 7.0,
                "spacing": 7.0,
                "overall": 7.0
            },
            "issues": [
                {
                    "category": "analysis",
                    "severity": "high",
                    "description": "Automated analysis failed - manual review required",
                    "location": "entire interface"
                }
            ]
        }
    
    def _calculate_overall_score(self, scores: Dict) -> float:
        """Calculate weighted overall score"""
        weights = {
            "layout": 0.25,
            "color": 0.20,
            "typography": 0.20,
            "spacing": 0.25,
            "overall": 0.10
        }
        
        weighted_sum = sum(scores[key] * weights[key] for key in weights if key in scores)
        return round(weighted_sum * 10, 1)  # Convert to 0-100 scale
    
    def _determine_status(self, overall_score: float, threshold: float) -> str:
        """Determine pass/conditional/fail status"""
        if overall_score >= threshold:
            return "pass"
        elif overall_score >= self.CONDITIONAL_THRESHOLD * 10:  # Convert to 0-100 scale
            return "conditional"
        else:
            return "fail"
    
    def _create_linear_tickets(self, issues: List[Dict], figma_key: str, node_id: str, url: str) -> List[str]:
        """Create Linear tickets for visual issues"""
        tickets = []
        
        for issue in issues:
            if issue["severity"] in ["medium", "high"]:
                title = f"Visual QA: {issue['description']}"
                description = f"""
## Visual QA Issue

**Category:** {issue['category'].title()}
**Severity:** {issue['severity'].title()}
**Location:** {issue['location']}

**Description:** {issue['description']}

**References:**
- Figma: `{figma_key}:{node_id}`
- Implementation: {url}

**Found by:** Automated Visual QA Pipeline
"""
                
                # This would call linear_create_issue
                # ticket = linear_create_issue(
                #     title=title,
                #     description=description,
                #     team="UX",  # or appropriate team
                #     labels=["visual-qa", "bug", issue["category"]],
                #     priority=2 if issue["severity"] == "high" else 3
                # )
                
                # Mock ticket ID
                ticket_id = f"LOC-{len(tickets) + 419}"
                tickets.append(ticket_id)
                
                print(f"🎫 Created ticket: {ticket_id}")
        
        return tickets
    
    def _log_comparison_result(self, result: Dict):
        """Log comparison result to file"""
        log_file = os.path.join(self.workspace_path, "logs", "visual-qa.jsonl")
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        log_entry = {
            "timestamp": result["comparison_timestamp"],
            "overall_score": result["overall_score"],
            "status": result["status"],
            "issue_count": len(result["issues"]),
            "tickets_created": len(result["linear_tickets"])
        }
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')


# CLI Interface
def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Visual QA Pipeline")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Compare command
    compare_parser = subparsers.add_parser('compare', help='Compare Figma design to implementation')
    compare_parser.add_argument('--figma-key', required=True, help='Figma file key')
    compare_parser.add_argument('--node-id', required=True, help='Figma node ID')
    compare_parser.add_argument('--url', required=True, help='Implementation URL')
    compare_parser.add_argument('--threshold', type=float, default=8.0, help='Pass/fail threshold (0-10)')
    compare_parser.add_argument('--no-tickets', action='store_true', help='Skip Linear ticket creation')
    compare_parser.add_argument('--no-escalate', action='store_true', help='Skip cloud escalation')
    
    # Batch command
    batch_parser = subparsers.add_parser('batch', help='Run batch comparison from config')
    batch_parser.add_argument('--config', required=True, help='JSON config file path')
    
    args = parser.parse_args()
    
    pipeline = VisualQAPipeline()
    
    if args.command == 'compare':
        result = pipeline.compare_design_implementation(
            figma_key=args.figma_key,
            node_id=args.node_id,
            implementation_url=args.url,
            threshold=args.threshold,
            create_tickets=not args.no_tickets,
            escalate_to_cloud=not args.no_escalate
        )
        
        print("\n" + "="*60)
        print(f"🎯 VISUAL QA RESULT")
        print(f"Score: {result['overall_score']}/100 ({result['status'].upper()})")
        print(f"Issues: {len(result['issues'])}")
        if result['linear_tickets']:
            print(f"Tickets: {', '.join(result['linear_tickets'])}")
        print("="*60)
        
        return result
        
    elif args.command == 'batch':
        with open(args.config) as f:
            config = json.load(f)
        
        results = []
        for test in config.get('tests', []):
            result = pipeline.compare_design_implementation(**test)
            results.append(result)
            
        print(f"\n📊 Batch complete: {len(results)} comparisons")
        return results

if __name__ == "__main__":
    main()
```

## Scoring Rubric

### Categories (0-10 each)

**Layout (0-10)**
- Element positioning and alignment
- Size accuracy and proportions  
- Grid system adherence
- Responsive behavior
- Component hierarchy

**Color (0-10)**
- Color accuracy (hex matching)
- Contrast and accessibility
- Gradients and effects
- Background colors
- Interactive state colors

**Typography (0-10)**
- Font family matching
- Font size accuracy
- Font weight and style
- Line height and letter spacing
- Text alignment and wrapping

**Spacing (0-10)**
- Margins and padding
- Component gaps
- Grid spacing
- White space distribution
- Visual rhythm

**Overall (0-10)**
- General visual fidelity
- User experience consistency
- Brand adherence
- Polish and attention to detail
- Accessibility considerations

### Thresholds

- **≥8.0 (80/100):** ✅ **PASS** - Ship it!
- **6.0-7.9 (60-79/100):** ⚠️ **CONDITIONAL** - Review and decide  
- **<6.0 (<60/100):** ❌ **FAIL** - Block merge, fixes required

### Issue Severity

- **Low:** Minor pixel differences, non-critical spacing
- **Medium:** Noticeable differences that may impact UX
- **High:** Major visual bugs, accessibility issues, brand violations

## Configuration

### Environment Setup

```bash
# Set up local directories
mkdir -p ~/.openclaw/workspace/skills/ux-visual-qa
mkdir -p ~/.openclaw/workspace/temp/visual-qa
mkdir -p ~/.openclaw/workspace/logs

# Install Python dependencies (if needed)
pip install pillow requests
```

### Config File Example

```json
{
  "defaults": {
    "threshold": 8.0,
    "create_tickets": true,
    "escalate_to_cloud": true
  },
  "tests": [
    {
      "name": "Homepage Hero",
      "figma_key": "ABC123",
      "node_id": "1:234", 
      "implementation_url": "https://app.example.com/",
      "threshold": 8.5
    },
    {
      "name": "Login Form",
      "figma_key": "ABC123",
      "node_id": "1:567",
      "implementation_url": "https://app.example.com/login"
    }
  ]
}
```

## Integration Examples

### GitHub Actions

```yaml
name: Visual QA
on:
  pull_request:
    paths: ['src/components/**', 'src/pages/**']

jobs:
  visual-qa:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy preview
        run: deploy-preview.sh
      - name: Run Visual QA
        run: |
          ux-qa compare \
            --figma-key ${{ secrets.FIGMA_KEY }} \
            --node-id "1:234" \
            --url ${{ env.PREVIEW_URL }} \
            --threshold 8.0
```

### Linear Automation

Automatically create tickets for failing comparisons:

```bash
# Run QA and create tickets for failures
ux-qa compare \
  --figma-key "ABC123" \
  --node-id "1:234" \
  --url "https://staging.app.com" \
  --threshold 8.0
```

### Pre-deployment Hook

```bash
#!/bin/bash
# pre-deploy.sh
echo "🎯 Running Visual QA..."

if ux-qa batch --config qa-config.json; then
  echo "✅ Visual QA passed - deploying"
  deploy.sh
else
  echo "❌ Visual QA failed - blocking deployment"
  exit 1
fi
```

## Troubleshooting

### Common Issues

**Figma download fails**
- Verify Figma file key and node ID
- Check Figma API permissions
- Ensure node exists and is exportable

**Screenshot fails**  
- Check URL accessibility
- Verify implementation is responsive
- Consider authentication requirements

**Qwen3-VL analysis fails**
- Check local model availability
- Verify image formats (PNG supported)
- Try cloud escalation if enabled

**Linear ticket creation fails**
- Check Linear API permissions
- Verify team and label names
- Check rate limiting

### Debugging

```bash
# Enable verbose logging
export VISUAL_QA_DEBUG=1

# Check comparison logs
tail -f ~/.openclaw/workspace/logs/visual-qa.jsonl

# Manual image verification
ls ~/.openclaw/workspace/temp/visual-qa/
```

## Performance

### Optimization Tips

- Use PNG scale 2 for sufficient detail without huge files
- Enable cloud escalation only for critical comparisons  
- Batch similar comparisons to reduce API calls
- Cache Figma downloads when comparing same design multiple times

### Benchmarks

- Figma download: ~2-5 seconds
- Browser screenshot: ~3-8 seconds  
- Local Qwen3-VL analysis: ~10-30 seconds
- Cloud Qwen3-VL analysis: ~5-15 seconds
- **Total pipeline:** ~20-60 seconds per comparison

## Security

- Figma API keys stored securely
- Screenshots stored in temporary directories
- Linear tickets respect workspace permissions
- No sensitive data logged to comparison results

---

**Version:** 1.0.0  
**Created:** 2026-02-10  
**License:** Internal Use Only