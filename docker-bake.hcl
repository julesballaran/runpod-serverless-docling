variable "REGISTRY" {
  default = "docker.io"
}

variable "REGISTRY_USER" {
  default = ""
}

variable "REPO_NAME" {
  default = ""
}

variable "RELEASE" {
  default = "0.0.2"
}

target "default" {
  dockerfile = "Dockerfile"
  tags = ["${REGISTRY}/${REGISTRY_USER}/${REPO_NAME}:${RELEASE}"]
  platforms = ["linux/amd64"]
  annotations = ["org.opencontainers.image.authors=${REGISTRY_USER}"]
}