terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

resource "docker_image" "app" {
  name = "devops-lab-app:v1"
}

resource "docker_container" "app" {
  name  = "devops-lab-tf"
  image = docker_image.app.image_id

  ports {
    internal = 5000
    external = 5050
  }
}
