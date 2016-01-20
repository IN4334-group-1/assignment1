
library(pls)
library(nnet)


linear.loop <- function(model, data, runs=10) {
	results = c();

	for (i in 1:runs) {
		sample.train <- sample(nrow(data), size = 0.5 * nrow(data))
	    train.data <- data[sample.train,]
	    test.data <- data[-sample.train,]

	    linearModel <- lm(model, data=train.data, na.action=na.omit)
		linearModel$xlevels[["country_code"]] <- union(linearModel$xlevels[["country_code"]], levels(ds$country_code))
		linearModel$xlevels[["language"]] <- union(linearModel$xlevels[["language"]], levels(ds$language))
		linearModel$xlevels[["domains"]] <- union(linearModel$xlevels[["language"]], levels(ds$domains))

		linearPrediction <- predict(linearModel, newdata=test.data, na.action=na.omit)

		predictions.lm.ds <- as.data.frame(linearPrediction)
		predictions.lm.ds$index <- as.numeric(rownames(predictions.lm.ds))
		predictions.lm.ds <- predictions.lm.ds[with(predictions.lm.ds, order(index)),]

		testDataMean <- mean(test.data[rownames(predictions.lm.ds),]$stars) #predictions.lm.ds is een dataframe met resultaten
		SSTot <- sum((test.data[rownames(predictions.lm.ds),]$stars - testDataMean)^2) 
		SSRes <- sum((test.data[rownames(predictions.lm.ds),]$stars - predictions.lm.ds$linearPrediction)^2)
		results[i] <- (1 - SSRes/SSTot) 
	}
	results
}

stepwise.loop <- function(model, data, runs=10) {
	results = c();

	for (i in 1:runs) {
		sample.train <- sample(nrow(data), size = 0.5 * nrow(data))
	    train.data <- data[sample.train,]
	    test.data <- data[-sample.train,]

	    linearModel <- lm(model, data=train.data, na.action=na.omit)
		linearModel$xlevels[["country_code"]] <- union(linearModel$xlevels[["country_code"]], levels(ds$country_code))
		linearModel$xlevels[["language"]] <- union(linearModel$xlevels[["language"]], levels(ds$language))
		linearModel$xlevels[["domains"]] <- union(linearModel$xlevels[["language"]], levels(ds$domains))

		stepModel <- step(linearModel, na.action=na.omit)

		linearPrediction <- predict(stepModel, newdata=test.data, na.action=na.omit)

		predictions.lm.ds <- as.data.frame(linearPrediction)
		predictions.lm.ds$index <- as.numeric(rownames(predictions.lm.ds))
		predictions.lm.ds <- predictions.lm.ds[with(predictions.lm.ds, order(index)),]

		testDataMean <- mean(test.data[rownames(predictions.lm.ds),]$stars) #predictions.lm.ds is een dataframe met resultaten
		SSTot <- sum((test.data[rownames(predictions.lm.ds),]$stars - testDataMean)^2) 
		SSRes <- sum((test.data[rownames(predictions.lm.ds),]$stars - predictions.lm.ds$linearPrediction)^2)
		results[i] <- (1 - SSRes/SSTot) 
	}
	results
}

pcr.loop <- function(model, data, runs=10) {

	results = c()

	for (i in 1:runs) {
		sample.train <- sample(nrow(data), size = 0.5 * nrow(data))
	    train.data <- data[sample.train,]
	    test.data <- data[-sample.train,]

	    pcrModel <- pcr(model, data=train.data, na.action = na.omit)
		pcrModel$xlevels[["country_code"]] <- union(pcrModel$xlevels[["country_code"]], levels(ds$country_code))
		pcrModel$xlevels[["language"]] <- union(pcrModel$xlevels[["language"]], levels(ds$language))
		pcrModel$xlevels[["domains"]] <- union(pcrModel$xlevels[["language"]], levels(ds$domains))

		pcrPrediction <- predict(pcrModel, newdata=test.data, ncomp=50, na.action = na.omit)

		predictions.pcr.ds <- as.data.frame(pcrPrediction)
		predictions.pcr.ds$index <- as.numeric(rownames(predictions.pcr.ds))
		predictions.pcr.ds <- predictions.pcr.ds[with(predictions.pcr.ds, order(index)),]

		testDataMean <- mean(test.data[rownames(predictions.pcr.ds),]$stars) #predictions.lm.ds is een dataframe met resultaten
		SSTot <- sum((test.data[rownames(predictions.pcr.ds),]$stars - testDataMean)^2) 
		SSRes <- sum((test.data[rownames(predictions.pcr.ds),]$stars - predictions.pcr.ds$`stars.50 comps`)^2)
		results[i] <- (1 - SSRes/SSTot)
	}
	results
}

plsr.loop <- function(model, data, runs=10) {

	results = c()

	for (i in 1:runs) {
		sample.train <- sample(nrow(data), size = 0.5 * nrow(data))
	    train.data <- data[sample.train,]
	    test.data <- data[-sample.train,]

	    plsrModel <- plsr(model, data=train.data, na.action = na.omit)
		plsrModel$xlevels[["country_code"]] <- union(plsrModel$xlevels[["country_code"]], levels(ds$country_code))
		plsrModel$xlevels[["language"]] <- union(plsrModel$xlevels[["language"]], levels(ds$language))
		plsrModel$xlevels[["domains"]] <- union(plsrModel$xlevels[["language"]], levels(ds$domains))

		plsrPrediction <- predict(plsrModel, newdata=test.data, ncomp=50, na.action = na.omit)

		predictions.plsr.ds <- as.data.frame(plsrPrediction)
		predictions.plsr.ds$index <- as.numeric(rownames(predictions.plsr.ds))
		predictions.plsr.ds <- predictions.plsr.ds[with(predictions.plsr.ds, order(index)),]

		testDataMean <- mean(test.data[rownames(predictions.plsr.ds),]$stars) #predictions.lm.ds is een dataframe met resultaten
		SSTot <- sum((test.data[rownames(predictions.plsr.ds),]$stars - testDataMean)^2) 
		SSRes <- sum((test.data[rownames(predictions.plsr.ds),]$stars - predictions.plsr.ds$`stars.50 comps`)^2)
		results[i] <- (1 - SSRes/SSTot)
	}
	results
}

nn.loop <- function(model, data, runs=10) {

	results = c()
	for (i in 1:runs) {
		sample.train <- sample(nrow(data), size = 0.5 * nrow(data))
	    train.data <- data[sample.train,]
	    test.data <- data[-sample.train,]

	    nnModel <- nnet(model, data=train.data, size=4, decay=0.0001, maxit=5000)

		nnPredictions <- predict(nnModel, test.data[,2:18])
		predictions.nn.ds <- as.data.frame(nnPredictions)
		predictions.nn.ds$index <- as.numeric(rownames(predictions.nn.ds))
		predictions.nn.ds <- predictions.nn.ds[with(predictions.nn.ds, order(index)),]
		predictions.nn.ds <- predictions.nn.ds[complete.cases(predictions.nn.ds),]

		testDataMean <- mean(test.data[rownames(predictions.nn.ds),]$stars) #predictions.lm.ds is een dataframe met resultaten
		SSTot <- sum((test.data[rownames(predictions.nn.ds),]$stars - testDataMean)^2) 
		SSRes <- sum((test.data[rownames(predictions.nn.ds),]$stars - predictions.nn.ds$V1)^2)
		results[i] <- (1 - SSRes/SSTot)
	}

	results


}