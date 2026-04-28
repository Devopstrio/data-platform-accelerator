provider "azurerm" {
  features {}
}

provider "aws" {
  region = var.aws_region
}

resource "azurerm_resource_group" "accelerator" {
  name     = "rg-${var.project_name}-accelerator-${var.environment}"
  location = var.location
}

# --- Accelerator Control Plane (AKS) ---

resource "azurerm_kubernetes_cluster" "accelerator_k8s" {
  name                = "aks-data-launchpad-${var.environment}"
  location            = azurerm_resource_group.accelerator.location
  resource_group_name = azurerm_resource_group.accelerator.name
  dns_prefix          = "launchpad-k8s"

  default_node_pool {
    name       = "default"
    node_count = 3
    vm_size    = "Standard_D4s_v3"
  }

  identity {
    type = "SystemAssigned"
  }
}

# --- Accelerator Metadata Store (Postgres) ---

resource "azurerm_postgresql_flexible_server" "metadata" {
  name                   = "psql-launchpad-metadata-${var.environment}"
  resource_group_name    = azurerm_resource_group.accelerator.name
  location               = azurerm_resource_group.accelerator.location
  version                = "13"
  administrator_login    = "lpadmin"
  administrator_password = var.db_password
  storage_mb             = 32768
  sku_name               = "GP_Standard_D2ds_v4"
}

# --- Multi-Cloud Storage Foundation (ADLS / S3) ---

resource "azurerm_storage_account" "datalake" {
  name                     = "stdatalake${var.environment}"
  resource_group_name      = azurerm_resource_group.accelerator.name
  location                 = azurerm_resource_group.accelerator.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  is_hns_enabled           = true # Enable ADLS Gen2
}

resource "aws_s3_bucket" "datalake_aws" {
  bucket = "data-launchpad-lake-${var.environment}"
}
