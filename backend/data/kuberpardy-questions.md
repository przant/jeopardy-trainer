# Kuberpardy Question Bank - MVP

## Q001 [basic] [fill-blank]
**Question:** Complete the command to get all pods:

```bash
kubectl ___ pods
```

**Answer:** get
**Explanation:** `kubectl get pods` lists pods in current namespace. Add `-A` or `--all-namespaces` for cluster-wide view. Add `-o wide` for node IPs.

---

## Q002 [basic] [multiple-choice]
**Question:** What does ImagePullBackOff mean?

**Options:**
A) Container crashed
B) Cannot pull image from registry
C) Out of memory
D) Node failure

**Answer:** B
**Explanation:** ImagePullBackOff indicates Kubernetes can't fetch the container image. Common causes: wrong image name, registry auth failure, network issues.

---

## Q003 [intermediate] [fill-blank]
**Question:** What command shows why a pod failed?

```bash
kubectl ________ pod <name>
```

**Answer:** describe
**Explanation:** `kubectl describe pod` shows events, which explain failures (image pull errors, scheduling issues, crashes). More detailed than `get`.

---

## Q004 [basic] [multiple-choice]
**Question:** What's the default Kubernetes Service type?

**Options:**
A) NodePort
B) LoadBalancer
C) ClusterIP
D) ExternalName

**Answer:** C
**Explanation:** ClusterIP is default - internal-only access. NodePort exposes on node IPs. LoadBalancer uses cloud provider LB. ExternalName creates DNS alias.

---

## Q005 [intermediate] [multiple-choice]
**Question:** Service has no endpoints. Most likely cause?

**Options:**
A) Firewall blocking traffic
B) Service selector doesn't match pod labels
C) Ingress misconfigured
D) Node is down

**Answer:** B
**Explanation:** Service uses selector to find pods. If labels don't match exactly, no endpoints created. Check with `kubectl get pods --show-labels` and compare to Service selector.

---

## Q006 [basic] [fill-blank]
**Question:** Check if Service has registered pod IPs:

```bash
kubectl get _________ <service-name>
```

**Answer:** endpoints
**Explanation:** `kubectl get endpoints` shows pod IPs behind Service. Empty = no pods matched selector. Use to debug Service → Pod connection.

---

## Q007 [intermediate] [multiple-choice]
**Question:** Pod shows 0/1 READY. What does this mean?

**Options:**
A) Pod hasn't started
B) Readiness probe failing
C) Container crashed
D) Out of disk space

**Answer:** B
**Explanation:** 0/1 means container running but readiness probe failing. Pod exists but not receiving traffic from Service. Check probe config and app startup.

---

## Q008 [gotcha] [multiple-choice]
**Question:** You delete a pod. What happens?

**Options:**
A) Pod permanently deleted
B) ReplicaSet creates replacement pod
C) Deployment scales down
D) Service stops working

**Answer:** B
**Explanation:** If pod managed by ReplicaSet/Deployment, controller immediately creates replacement to maintain desired count. Killing pods doesn't reduce replicas.

---

## Q009 [basic] [multiple-choice]
**Question:** What's the difference between Deployment and StatefulSet?

**Options:**
A) Deployment for apps, StatefulSet for storage
B) StatefulSet gives pods stable names and identity
C) StatefulSet is faster
D) No difference, just naming

**Answer:** B
**Explanation:** StatefulSet provides ordered pod names (app-0, app-1), stable network identity, and dedicated storage per pod. Use for databases. Deployment gives random names.

---

## Q010 [basic] [fill-blank]
**Question:** View logs from a pod:

```bash
kubectl ____ <pod-name>
```

**Answer:** logs
**Explanation:** `kubectl logs <pod>` shows stdout/stderr from container. Add `--previous` for crashed container logs. Add `-f` to follow (tail).

---

## Q011 [intermediate] [multiple-choice]
**Question:** PVC stuck in Pending. What's wrong?

**Options:**
A) Pod not scheduled
B) No StorageClass available
C) Service misconfigured
D) Image pull failure

**Answer:** B
**Explanation:** PVC needs StorageClass to provision volume. Check `kubectl get storageclass`. Install provisioner (like local-path-provisioner) or create PV manually.

---

## Q012 [gotcha] [multiple-choice]
**Question:** You scale Deployment to 3 replicas. Ingress only routes to one pod. Why?

**Options:**
A) Ingress caches pod IP
B) Service selector wrong
C) Pods not ready yet
D) This is normal behavior

**Answer:** C
**Explanation:** Ingress routes through Service, which only includes READY pods (passing readiness probe). Check pod status - likely 0/3 or 1/3 ready. Other pods starting or failing probes.

---

## Q013 [basic] [multiple-choice]
**Question:** How do you expose a Deployment externally in homelab?

**Options:**
A) ClusterIP Service
B) NodePort Service
C) kubectl expose only
D) Edit Deployment directly

**Answer:** B
**Explanation:** NodePort exposes on node IP at static port (30000-32767). No cloud provider needed. ClusterIP is internal only. LoadBalancer needs cloud or MetalLB.

---

## Q014 [intermediate] [fill-blank]
**Question:** Create secret from literal values:

```bash
kubectl create secret ______ <name> --from-literal=key=value
```

**Answer:** generic
**Explanation:** `generic` (aka Opaque) is most common secret type. Other types: `docker-registry` for registry auth, `tls` for certificates.

---

## Q015 [basic] [multiple-choice]
**Question:** What does a liveness probe do?

**Options:**
A) Checks if pod should receive traffic
B) Checks if container should be restarted
C) Checks resource usage
D) Checks network connectivity

**Answer:** B
**Explanation:** Liveness probe restarts container if failing (app deadlocked but process alive). Readiness probe removes from Service if failing (app not ready for traffic).

---

## Q016 [intermediate] [multiple-choice]
**Question:** Why use imagePullSecrets?

**Options:**
A) Encrypt container images
B) Authenticate to private registry
C) Speed up image pulls
D) Required for StatefulSets

**Answer:** B
**Explanation:** Private registries need credentials. Create secret: `kubectl create secret docker-registry <name>`, then reference in pod spec with `imagePullSecrets`.

---

## Q017 [gotcha] [multiple-choice]
**Question:** Deployment updated but pods still running old version. Why?

**Options:**
A) Update didn't apply
B) Need to restart pods manually
C) Rolling update in progress (check rollout status)
D) Image tag unchanged

**Answer:** C or D
**Explanation:** Both valid. If image tag unchanged (using `latest`), Kubernetes won't pull. Use digest or versioned tags. Or rolling update still in progress - check `kubectl rollout status deployment/<name>`.

---

## Q018 [basic] [fill-blank]
**Question:** Get pod IP addresses and node placement:

```bash
kubectl get pods -o ____
```

**Answer:** wide
**Explanation:** `-o wide` shows additional columns: IP, NODE, NOMINATED NODE, READINESS GATES. Alternative: `-o yaml` or `-o json` for full details.

---

## Q019 [intermediate] [multiple-choice]
**Question:** What's the correct order to debug "Service not reachable"?

**Options:**
A) Check Ingress → Service → Endpoints → Pods
B) Check Pods → Endpoints → Service → Ingress
C) Check Firewall → DNS → Pods → Service
D) Just restart everything

**Answer:** B
**Explanation:** Bottom-up debugging: Verify pods running → endpoints populated → service configured → ingress routing. Start from infrastructure, move toward edge.

---

## Q020 [basic] [multiple-choice]
**Question:** What does CrashLoopBackOff mean?

**Options:**
A) Pod scheduled but image can't pull
B) Container repeatedly crashing and restarting
C) Node out of resources
D) Readiness probe failing

**Answer:** B
**Explanation:** Container starts, crashes, Kubernetes restarts it with exponential backoff. Check logs: `kubectl logs <pod> --previous` to see crash reason.

---

## Q021 [intermediate] [fill-blank]
**Question:** Decode a secret value:

```bash
kubectl get secret <n> -o jsonpath='{.data.key}' | base64 __
```

**Answer:** -d
**Explanation:** Kubernetes stores secrets base64-encoded. `-d` or `--decode` flag decodes to plaintext. Without it, you see gibberish.

---

## Q022 [gotcha] [multiple-choice]
**Question:** You apply a ConfigMap change. Pods don't see new values. Why?

**Options:**
A) Need to restart pods
B) ConfigMap takes 10 minutes to propagate
C) Must delete and recreate ConfigMap
D) Pods cache ConfigMap indefinitely

**Answer:** A
**Explanation:** Mounted ConfigMaps update eventually (~1 minute), but environment variables from ConfigMaps don't update until pod restart. Restart pods to see changes.

---

## Q023 [basic] [multiple-choice]
**Question:** What's a Headless Service (clusterIP: None)?

**Options:**
A) Service without endpoints
B) Returns pod IPs directly, no load balancing
C) External service only
D) Broken service configuration

**Answer:** B
**Explanation:** Headless Service returns all pod IPs via DNS (no virtual IP). Used for StatefulSets where clients need direct pod access (databases).

---

## Q024 [intermediate] [multiple-choice]
**Question:** Ingress returns 502 Bad Gateway. What's wrong?

**Options:**
A) Ingress controller crashed
B) Service exists but no healthy pods
C) DNS resolution failed
D) Certificate expired

**Answer:** B
**Explanation:** 502 = Ingress reached Service but can't connect to backend. Common causes: no pods ready, service selector wrong, pods listening on wrong port.

---

## Q025 [basic] [fill-blank]
**Question:** Port-forward to access pod locally:

```bash
kubectl port-forward pod/<name> ____:8080
```

**Answer:** 8080
**Explanation:** Format: `local-port:pod-port`. Example: `8080:8080` maps localhost:8080 to pod's port 8080. Use for debugging without exposing Service.

---

## Q026 [intermediate] [multiple-choice]
**Question:** What's the purpose of a readiness probe?

**Options:**
A) Restart unhealthy containers
B) Determine if pod should receive traffic
C) Monitor resource usage
D) Schedule pod on node

**Answer:** B
**Explanation:** Readiness probe controls Service endpoint registration. Failing probe = pod removed from Service (no traffic). Pod keeps running. Use during app startup/warm-up.

---

## Q027 [gotcha] [multiple-choice]
**Question:** All pods healthy but Ingress hostname doesn't resolve. Issue?

**Options:**
A) Pods not ready
B) DNS not configured for hostname
C) Ingress controller not installed
D) Service selector wrong

**Answer:** B
**Explanation:** Ingress doesn't create DNS records. You must configure DNS (hosts file, local DNS, real DNS) to point hostname to Ingress controller IP or node IP.

---

## Q028 [basic] [multiple-choice]
**Question:** How do you scale a Deployment?

**Options:**
A) kubectl scale deployment <name> --replicas=3
B) kubectl set replicas <name> 3
C) kubectl update deployment <name> replicas=3
D) Edit pod directly

**Answer:** A
**Explanation:** `kubectl scale deployment <name> --replicas=N` adjusts replica count. Alternative: `kubectl edit deployment <name>` and change `spec.replicas`.

---

## Q029 [intermediate] [multiple-choice]
**Question:** Why use a startup probe?

**Options:**
A) Speed up pod startup
B) Disable liveness probe during slow startup
C) Check network connectivity
D) Required for all containers

**Answer:** B
**Explanation:** Startup probe runs first, disabling liveness checks. Prevents killing slow-starting apps (legacy apps, large data loads). Once passes, liveness/readiness take over.

---

## Q030 [intermediate] [fill-blank]
**Question:** Check rollout status after updating Deployment:

```bash
kubectl _______ status deployment/<name>
```

**Answer:** rollout
**Explanation:** `kubectl rollout status` shows rolling update progress. Also: `kubectl rollout history` (past versions), `kubectl rollout undo` (rollback).