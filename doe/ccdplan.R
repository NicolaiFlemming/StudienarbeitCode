library(rsm)

#Central Composite Design

dsg2 <- ccd(2, n0 = 1, randomize = FALSE, alpha = "rotatable")
View(dsg2)

is_center <- (dsg2$x1 == 0) & (dsg2$x2 == 0)

# Identify which rows to keep: all non-center points OR the first instance of the center point
rows_to_keep <- !is_center | !duplicated(dsg2[, c("x1", "x2")])

# Filter the design to keep only the unique center point
dsg2 <- dsg2[rows_to_keep, ]

# 2. Map and Round natural variables (as before)
dsg2$Overlap <- round(15 * dsg2$x1 + 45, 2)
dsg2$Adhesive <- "DP490"
dsg2$Film_thickness <- round(0.125 * dsg2$x2 + 0.225, 2)
dsg2$Cores <- 28

# 3. Create a subset and save
output_data <- dsg2[ , c("Overlap", "Adhesive", "Film_thickness", "Cores")]
save_path <- "/Users/nicol/Documents/GitHub/StudienarbeitCode/abaqus-strapjoint-sim/inputs/sim_params.csv"

write.csv(output_data, save_path, row.names = FALSE, quote = FALSE)