library(jsonlite)

config <- NULL

load_config <- function() {
  config_path <- "src/config.json"
  if (!file.exists(config_path)) {
    stop(paste0("Config file not found: ", config_path))
  }
  cfg <- fromJSON(config_path)
  config <<- cfg
  invisible(NULL)
}

get_wid_folderpath <- function() {
  if (is.null(config)) load_config()
  return(config$wid_folder)
}

get_ess_folderpath <- function() {
  if (is.null(config)) load_config()
  return(config$ess_folder)
}

get_output_folderpath <- function() {
  if (is.null(config)) load_config()
  return(config$output_folder)
}

get_output_folderpath_verification <- function() {
  if (is.null(config)) load_config()
  return(config$output_folder_verification)
}
