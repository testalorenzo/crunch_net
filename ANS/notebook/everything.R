par(mfrow = c(1, 1))

library(readr)
library(fda.usc)
library(reshape2)
library(tidyverse)
library(refund)
library(leaps)
library(caret)
library(stargazer)
library(amap)
library(cluster)

covariate <- read_csv("covariate.csv", col_types = cols(index = col_character()))
covariate <- covariate[,c(2,5,10:14,16,17)]
orginfo <- read_csv("orginfo.csv", col_types = cols(index = col_character()))
orginfo <- orginfo[,-c(1,3)]
regdata <- as.data.frame(covariate[,3:9])

data2 <- read_csv("aligned_data.csv") #aligned data
data2[is.na(data2)] <- 0
data2 <- sapply(data2, FUN=cumsum) #apply di cumulative sum sulle colonne
data2 <- data2[,-1]
#great0 <- data2[20,]>0
#data2 <- data2[,great0]
matplot(as.matrix(data2[1:10,]), type='l')

hist(log(orginfo$voterank))
hist(log(orginfo$eigenvector+0.01))
hist(log(orginfo$degree))
hist(log(orginfo$pagerank))
hist(orginfo$closeness)
hist(log(orginfo$newman+0.001))
hist(log(orginfo$subgraph)) # away
hist(log(orginfo$average))

hist(log(regdata$eigen_max+0.01))
hist(log(regdata$pages_max+0.001))
hist(log(regdata$degcen_max+0.01))
hist(log(regdata$bet_max+0.001))
hist(log(regdata$avg_max+1))
hist(regdata$newman_max)

dt <- merge(orginfo, covariate, 'index') #merging 

#Trasformazione logaritmica - normalizzi

dt['eigen_max'] <- log(dt$eigen_max+0.01)
dt['pages_max'] <- log(dt$pages_max+0.001)
dt['degcen_max'] <- log(dt$degcen_max+0.01)
dt['bet_max'] <- log(dt$bet_max+0.001)
dt['avg_max'] <- log(dt$avg_max+1)
dt['newman_max'] <- dt$newman_max
dt['voterank'] <- log(dt$voterank)
dt['eigenvector'] <- log(dt$eigenvector+0.01)
dt['degree'] <- log(dt$degree)
dt['pagerank'] <- log(dt$pagerank)
dt['newman'] <- log(dt$newman+0.001)
dt['subgraph'] <- log(dt$subgraph)
dt['average'] <- log(dt$average)

dt <- dt[,-c(10,17)] #tolto colonne


cumulate <- data2[10,] #decima riga
cumulate <- as.data.frame(cumulate)
cumulate['index'] <- rownames(cumulate)
dt <- merge(dt, cumulate, by='index')

content <- read_csv("content.csv", col_types = cols(index_x = col_character())) #vivo o morto per industria

avg_per_sector <- read_csv("avg_per_sector.csv") 
avg_per_sector <- avg_per_sector[, c(1,2,4,7)]
avg_per_sector[is.na(avg_per_sector)] <- 0
avg_per_sector <- avg_per_sector %>%
  group_by(industry) %>%
  mutate(c_sum=cumsum(size_real_x))
avg_per_sector1 <- dcast(avg_per_sector, date_y ~ industry, value.var = 'c_sum')
avg_per_sector2 <- dcast(avg_per_sector, date_y ~ industry, value.var = 'size_real_y')
avg_per_sector1 <- avg_per_sector1[,-1]
avg_per_sector2 <- avg_per_sector2[,-1]

matplot(as.matrix(avg_per_sector1[1:10,]), type='l')


# FUNCTIONAL CLUSTERING
out.fd2=kmeans.fd(t(as.matrix(data2[1:10,])),ncl=2,draw=TRUE)
clu <- as.data.frame(out.fd2$cluster)
clu['index'] <- rownames(clu)

par(mfrow = c(1, 1))
for (ind in unique(content$industry)) {
  idx <- unique(content$index_x[content$industry==ind])
  cl <- alive[idx]
  mat <- data2[1:10, idx]
  indx <- str_replace_all(ind, "[[:punct:]]", " ")
  pdf(paste(indx, '.pdf'))
  matplot(mat, main=paste("Trajectories in",ind), type='l', lty=1, xlab = 'Time', ylab = 'Cumulative money raised')
  matplot(mat, main=paste("Trajectories in",ind), col=cl+2, type='l', lty=1)
  legend('topright', legend=unique(cl), col=c(unique(cl+2)), bty='n', pch=15)
  matr <- rowMeans(mat)
  lines(matr, lwd=3, col='black')
  dev.off()
}

par(mfrow = c(1, 1))
ind <- unique(content$industry)[1]
#clusters <- c()
for (ind in unique(content$industry)) {
  idx <- unique(content$index_x[content$industry==ind])
  mat <- data2[1:10, idx]
  indx <- str_replace_all(ind, "[[:punct:]]", " ")
  pdf(paste(indx, 'kmeans.pdf'))
  out.fd1=kmeans.fd(t(as.matrix(mat)),ncl=2,draw=TRUE, cluster.size = 1)
  dev.off()
  cl <- out.fd1$cluster
  if (out.fd1$centers$data[1,10]> out.fd1$centers$data[2,10]) {
    cl[which(cl==1)] <- 'H'
    cl[which(cl==2)] <- 'L'
  } else {
    cl[which(cl==1)] <- 'L'
    cl[which(cl==2)] <- 'H'
  }
  clusters <- append(clusters, cl)
}

clusters[clusters=='H'] <- 1
clusters[clusters=='L'] <- 0
sum(as.numeric(clusters))
log <- as.data.frame(clusters)
log['index'] <- rownames(log)
write.csv(log, 'log_response.csv')

#xi <- colnames(data2)
#write.csv(xi, 'xi.csv')


# LOGISTIC REGRESSION 
# Selecting variables
dt <- dt %>%
  mutate_if(is.numeric, scale)
cor(dt[,-1], use='complete.obs')
dt <- merge(dt, log, by='index')
rownames(dt) <- dt[,1]
dt <- dt[,-1]

d <- Dist(t(dt[,-c(15,16)]), method = "correlation")
hc1 <- hclust(d, method = "complete" )
plot(hc1, cex = 0.6, hang = -1)


model <- glm(as.numeric(dt$clusters) ~ dt$newman_max + dt$degcen_max + dt$eigenvector + dt$closeness, data = dt, family = binomial)
summary(model)
(model$null.deviance-model$deviance)/model$null.deviance
# Dealing with the imbalanced case
ory <- c(1:5)
oryp <- c(1:5)
dv <- c(1:5)
ory <- as.data.frame(ory)
oryp <- as.data.frame(oryp)
dv <- as.data.frame(dv)
for (i in 1:1000) {
  x <- sample(rownames(dt), length(dt$clusters[dt$clusters==1]), replace = FALSE, prob = NULL)
  sample_data <- dt[x,]
  pos <- dt[dt$clusters==1,]
  sample_data <- rbind(sample_data, pos)
  #model <- glm(as.numeric(clusters) ~ ., data = sample_data, family = binomial)
  #model_log <- glm(as.numeric(clusters) ~ log(sample_data$eigen_max+1)+log(sample_data$pages_max+1)+log(sample_data$degcen_max+1)+log(sample_data$bet_max+1)+log(sample_data$avg_max+1)+log(sample_data$newman_max+1)+log(sample_data$vote_min+1), data = sample_data, family = binomial)
  model <- glm(as.numeric(sample_data$clusters) ~ sample_data$newman_max + sample_data$degcen_max + sample_data$eigenvector + sample_data$closeness, data = sample_data, family = binomial)
  #model <- glm(as.numeric(sample_data$clusters) ~ log(sample_data$eigen_max+0.01), data = sample_data, family = binomial)
  summ <- summary(model)
  mem <- summ$coefficients[,1]
  pv <- summ$coefficients[,4]
  ory[i] <- mem
  oryp[i] <- pv
  dv[i] <- (summ$null.deviance-summ$deviance)/summ$null.deviance
}

dv <- t(dv)
hist(dv[,1])
summary(dv[,1])

oryt <-as.data.frame(t(as.matrix(ory)))
colnames(oryt) <- c("intercept", colnames(dt)[c(14,11,2,5)])
for (i in colnames(oryt)) {
  m <- mean(oryt[,i])
  std <- sd(oryt[,i])
  hist(oryt[,i], main=paste('Distribution of estimated coefficient of', i), xlab = i)
  abline(v=m, col='orange', lwd=2)
  abline(v=m+std, col='blue', lwd=2, lty=2)
  abline(v=m-std, col='blue', lwd=2, lty=2)
  abline(v=0, col='green', lwd=2)
}

orypt <-as.data.frame(t(as.matrix(oryp)))
for (i in colnames(orypt)) {
  m <- mean(orypt[,i])
  std <- sd(orypt[,i])
  hist(orypt[,i], main=paste('P-value distribution of', i), xlab = i)
  abline(v=m, col='orange', lwd=2)
}

par(mfrow = c(2, 3))
for (i in 1:5) {
  plot(oryt[,i],-log(orypt[,i]), xlab='Coefficient estimate', ylab='Significance', main=colnames(oryt)[i], pch=1, cex=0.1)
  m <- mean(oryt[,i])
  std <- sd(oryt[,i])
  abline(v=m, col='orange', lwd=2)
  abline(h=-log(0.1), col='blue', lwd=2)
  abline(v=m+std, col='orange', lwd=2, lty=2)
  abline(v=m-std, col='orange', lwd=2, lty=2)
  abline(v=0, col='green', lwd=2)
}

dvt <-as.data.frame(t(as.matrix(dv))) 
for (i in colnames(dvt)) {
  m <- mean(dvt[,i])
  std <- sd(dvt[,i])
  hist(dvt[,i], main=paste('Deviance distribution of', i), xlab = i)
  abline(v=m, col='orange', lwd=2)
}


# LINEAR REGRESSION - BEST SUBSET SELECTION
# move to linear as bad results and sample size
regsub <- regsubsets(dt$cum ~ ., data = dt[,-c(15,16)])
summary(regsub)
a <-lm(dt$cumulate ~ dt$newman_max +dt$voterank + dt$closeness + dt$eigenvector, dt)
b <- lm(dt$cumulate ~ dt$newman_max +dt$degcen_max + dt$closeness + dt$eigenvector, dt)
summary(a)
stargazer(a, b, type='latex')


# FUNCTION ON SCALAR
x=3
modmat=cbind(1,as.matrix(dt[!is.na(dt[,3]) & !is.na(dt[,12]),-c(15,16)]))
y=t(as.matrix(data2[1:10, rownames(dt[!is.na(dt[,3]) & !is.na(dt[,12]),])]))
olsmod = fosr(Y=y, X = modmat[,c(1,12,15, 3, 6)], method='OLS', lambda=0.000001)
plot(olsmod)
