# Complexity Router Examples

## High Complexity (8.21+ → Opus)

```bash
./route.sh "Design a distributed microservices architecture for LockN with service mesh, observability, and multi-tenant isolation"
# → Score: 9.5 → Escalates to complex-cloud (Opus)

./route.sh "Develop a comprehensive business strategy for scaling LockN to 100M users with international compliance"
# → Score: 9.8 → Escalates to complex-cloud (Opus)

./route.sh "Research and design a novel ML approach for real-time audio analysis with <1ms latency requirements"  
# → Score: 9.1 → Escalates to complex-cloud (Opus)
```

## Medium Complexity (≤8.20 → Sonnet)

```bash
./route.sh "Implement OAuth 2.0 authentication for the LockN API with proper error handling"
# → Score: 6.5 → Handled by Sonnet

./route.sh "Debug the WebSocket connection issue in lockn-score and fix the reconnection logic"
# → Score: 5.2 → Handled by Sonnet

./route.sh "Create a React dashboard component for displaying user statistics with charts"
# → Score: 4.8 → Handled by Sonnet
```

## Low Complexity (≤4.00 → Sonnet)

```bash
./route.sh "Check if port 11439 is responding and show the service status"
# → Score: 1.8 → Handled by Sonnet

./route.sh "List all running Docker containers and their memory usage"
# → Score: 2.1 → Handled by Sonnet

./route.sh "What's the current status of the GitHub Actions workflows?"
# → Score: 3.2 → Handled by Sonnet
```

## Integration

This can be used in main session logic to automatically route based on complexity:

```bash
# In session workflows
complexity-router "$USER_REQUEST"
```