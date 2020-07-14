#import required packages 
if (!require('Boruta')) install.packages('Boruta'); library('Boruta')
sed.seed(38)

#get data and summary 
traindata <- read.csv("data_after_cleaning_norm_dummy.csv", header = T, stringsAsFactors = F)
#traindata <- traindata[0:500,]
summary(traindata)
length(traindata)
#get cols and use this to make x and y data
cols <- c(colnames(traindata))
cols = cols[!(cols %in% c("dummy_next_start_time"))]
x <- traindata[cols]
y = traindata['dummy_next_start_time']

#Run algorithm 
boruta.output <- Boruta(x,as.vector(y$dummy_next_start_time),doTrace = 3, maxRuns = 50)
allCols <- colnames(boruta.output$ImpHistory)
colsNotUse <- c("shadowMax","shadowMin","shadowMean")
write.csv(attStats(boruta.output),'output_r.csv')


plot(boruta.output, xlab = "", xaxt = "n")
lz<-lapply(1:ncol(boruta.output$ImpHistory),function(i) boruta.output$ImpHistory[is.finite(boruta.outputn$ImpHistory[,i]),i])
names(lz) <- colnames(boruta.output$ImpHistory)
Labels <- sort(sapply(lz,median))
axis(side = 1,las=2,labels = names(Labels),at = 1:ncol(boruta.output$ImpHistory), cex.axis = 0.7)

plot(boruta.output, cex.axis=.7, las=2, xlab="", main="Variable Importance")  




plottt <- 
install.packages('zoom')



library(zoom)
zm(plottt)