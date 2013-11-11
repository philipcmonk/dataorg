args <- commandArgs(trailingOnly = TRUE)
trial <- args[1]
othertrials <- args[-1]
data <- read.csv(paste("XRD/Processed/",trial,".txt",sep=""),sep="",header = FALSE, skip=1, col.names = c("TwoTheta", "Intensity"))
png(paste("data/",trial,"_graph.png",sep=""))
plot(data$TwoTheta,data$Intensity,type="l",col="blue")
for (ot in othertrials){
	otdata <- read.csv(paste("XRD/Processed/",ot,".txt",sep=""),sep="",header = FALSE, skip=1, col.names = c("TwoTheta", "Intensity"))
	lines(otdata$TwoTheta,otdata$Intensity,col="red")
}
dev.off()

