{{/* Labels communs a tous les objets du chart (convention app.kubernetes.io/*). */}}
{{- define "stack.labels" -}}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
{{- end }}
