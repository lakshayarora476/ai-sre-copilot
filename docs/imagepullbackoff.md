# ImagePullBackOff Runbook

## Meaning

ImagePullBackOff means Kubernetes cannot pull the container image, so the pod cannot start.

## Common Causes

- Wrong image name
- Wrong image tag
- Image does not exist in registry
- Private registry authentication issue
- Missing imagePullSecret
- Registry is unavailable
- Network or DNS issue when reaching registry

## Useful Commands

- kubectl get pods -n <namespace>
- kubectl describe pod <pod-name> -n <namespace>
- kubectl get events -n <namespace> --sort-by=.lastTimestamp
- kubectl get secret -n <namespace>
- kubectl describe secret <secret-name> -n <namespace>

## Safe Next Steps

- Check the image name and tag
- Check pod events for image pull errors
- Verify image exists in the registry
- Verify imagePullSecret exists
- Check registry authentication
- Check network access to the registry

## What Not To Do

- Do not delete the namespace
- Do not restart random workloads before checking events
- Do not change image tags in production without approval