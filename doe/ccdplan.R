library(rsm)

#Central Composite Design

dsg2 <- ccd(2, n0 = 1, randomize = FALSE, alpha = "rotatable")

View(dsg2)

# Map natural variables
dsg2$Overlap <- 15*dsg2$x1 + 45
dsg2$Adhesive <- "DP490"
dsg2$Film_thickness <- 0.125*dsg2$x2 + 0.225
dsg2$Cores <- 28



output_data <- dsg2[ , c("Overlap", "Adhesive", "Film_thickness", "Cores")]
save_path <- "/Users/nicol/Documents/GitHub/StudienarbeitCode/abaqus-strapjoint-sim/inputs/sim_params.csv"

write.csv(output_data, save_path, row.names = FALSE, quote = FALSE)

