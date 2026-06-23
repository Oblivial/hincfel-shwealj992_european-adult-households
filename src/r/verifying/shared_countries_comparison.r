source("src/r/util/locationutil.r")
source("src/r/util/config.r")

table_countries_compare_by_year <- function(start_year) {
  stfeco_path <- paste0(get_output_folderpath(), "/stfeco_by_country_year.csv")
  shweal_path <- paste0(get_output_folderpath(), "/shweal_by_country_year.csv")

  if (!file.exists(stfeco_path) || !file.exists(shweal_path)) {
    stop("Processed data files not found in data/processed. Please generate stfeco_by_country_year.csv and shweal_by_country_year.csv first.")
  }

  stfeco <- read.csv(stfeco_path, stringsAsFactors = FALSE)
  shweal <- read.csv(shweal_path, stringsAsFactors = FALSE)

  stfeco$year <- as.numeric(stfeco$year)
  shweal$year <- as.numeric(shweal$year)
  start_year <- as.numeric(start_year)

  stfeco <- stfeco[stfeco$year > start_year, , drop = FALSE]
  shweal <- shweal[shweal$year > start_year, , drop = FALSE]

  # Restrict to European codes
  european_codes <- get_european_countrycodes_r()
  if (!is.null(european_codes) && length(european_codes) > 0) {
    stfeco <- stfeco[stfeco$country %in% european_codes, , drop = FALSE]
    shweal <- shweal[shweal$country %in% european_codes, , drop = FALSE]
  }

  ess_presence <- unique(stfeco[c("country", "year")])
  ess_presence$ess_exists <- TRUE

  wid_presence <- unique(shweal[c("country", "year")])
  wid_presence$wid_exists <- TRUE

  comparison <- merge(
    ess_presence,
    wid_presence,
    by = c("country", "year"),
    all = TRUE
  )

  comparison$ess_exists <- !is.na(comparison$ess_exists)
  comparison$wid_exists <- !is.na(comparison$wid_exists)

  comparison <- comparison[order(comparison$country, comparison$year), ]
  rownames(comparison) <- NULL
  return(comparison)
}

tbl_countries_years <- table_countries_compare_by_year(start_year = 2002)
output_path <- paste0(get_output_folderpath_verification(), "/shared_countries_comparison.csv")
write.csv2(tbl_countries_years, output_path, row.names = FALSE)