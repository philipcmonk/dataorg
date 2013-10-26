args <- commandArgs(trailingOnly = TRUE)
trial <- args[1]
data <- read.csv(paste("XRD/Processed/",trial,".txt",sep=""),sep="",header = FALSE, skip=1, col.names = c("TwoTheta", "Intensity"))
png(paste("data/",trial,"_graph.png",sep=""))
plot(data$TwoTheta,data$Intensity,type="l",col="red")
dev.off()

