library(reticulate)
use_virtualenv("./.venv", required = TRUE)
location_util <- import_from_path("util.locationutil", path = normalizePath("src/python"))

get_filtered_country_mapping_r <- function() {
  countries <- location_util$get_filtered_country_mapping()
  return(countries)
}

get_european_countrycodes_r <- function() {
  european_codes <- location_util$get_european_countrycodes()
  return(european_codes)
}