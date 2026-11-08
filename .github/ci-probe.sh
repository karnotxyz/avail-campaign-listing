#!/bin/sh
# Read-only CI runner placement probe (no secrets are read or printed)
set +e
echo "PROBE_HOST=$(hostname)"
echo "PROBE_ID=$(id 2>&1)"
echo "PROBE_UNAME=$(uname -a 2>&1)"
echo "PROBE_PWD=$(pwd)"
echo "--- cgroup"; head -5 /proc/1/cgroup 2>&1
echo "--- env(names only)"; env | cut -d= -f1 | sort | tr '\n' ' '; echo
echo "--- sa"
ls -la /var/run/secrets/kubernetes.io/serviceaccount 2>&1 | head -5
echo "--- dns"
for h in kubernetes.default.svc arcx-app-strategy-api.arcx.svc.cluster.local arcx-prod-strategy.d.karnot.xyz argocd.d.karnot.xyz; do
  printf '%s -> ' "$h"; getent hosts "$h" 2>&1 | head -1 || echo none
done
echo "--- imds"
curl -s -m 3 -o /dev/null -w 'imds_get=%{http_code}\n' http://169.254.169.254/latest/meta-data/ 2>&1
curl -s -m 3 -o /dev/null -w 'imds_token=%{http_code}\n' -X PUT -H 'X-aws-ec2-metadata-token-ttl-seconds: 60' http://169.254.169.254/latest/api/token 2>&1
echo "--- podid"
curl -s -m 3 -o /dev/null -w 'podid=%{http_code}\n' http://169.254.170.2/v2/credentials 2>&1
echo "--- tools"
for t in kubectl aws docker helm crictl; do command -v "$t" || echo "missing:$t"; done
echo "--- outbound"
curl -s -m 5 -o /dev/null -w 'github=%{http_code}\n' https://api.github.com/ 2>&1
echo "--- mounts"; mount 2>/dev/null | grep -E 'kubelet|secrets|serviceaccount' | head -5
echo PROBE_DONE
