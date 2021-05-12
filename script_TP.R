if (!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager")
BiocManager::install("DESeq2")
# file with the pseudo replicates 
library(readxl)
matrix = data.frame(read_excel(file.choose()), row.names = 1) #select the mean file
head(matrix)
dim(matrix)
# file with the metadata
coldata =  data.frame(read_excel(file.choose()), row.names = 1) #select the matrix file 
#get the tissue name
tissue = strsplit(colnames(matrix)[1],'_')[[1]][1]
#create deseq object
library("DESeq2")
dds <- DESeqDataSetFromMatrix(countData=matrix, colData=coldata, design= ~age)
#run deseq2
dds <- DESeq(dds)
dds

#dispersion plot
plotDispEsts(dds, main="Dispersion plot")#visualize the png

#pairwise comparaisons 
comparisons<- c('1m_VS_mean','3m_VS_mean','6m_VS_mean','9m_VS_mean','12m_VS_mean','15m_VS_mean','18m_VS_mean','21m_VS_mean','24m_VS_mean','27m_VS_mean')
#define directory for new files
dir <- "/home/kaouther/Documents/Internship/TP_brain"

#loop to create folder, store results and mitox file
for (dirname in comparisons){
  dir.create(paste(dir, dirname, sep=""))
  #set working directory
  setwd(paste(dir,dirname, sep=""))
  #choose the contrast
  first <- strsplit(dirname, "_VS_")[[1]][1]
  second <- strsplit(dirname, "_VS_")[[1]][2]
  res <- results(dds,c('age',first, second))
  ## Order by adjusted p-value
  
  res <- res[order(res$padj), ]
  
  ## Merge with normalized count data
  resdata <- merge(as.data.frame(res), as.data.frame(counts(dds, normalized=TRUE)), by="row.names", sort=FALSE)
  #compute the mean for condition
  resdata[paste("Mean_",second, sep="")]<-rowMeans(resdata[,as.character(coldata[coldata$age==second, "Name"])])
  resdata[paste("Mean_", first,sep="")]<-rowMeans(resdata[,as.character(coldata[coldata$age==first, "Name"])])
  colnames(resdata)[1]<-"Gene"
  write.table(resdata, file = paste("complete-results_",dim(resdata)[1],"_.txt", sep=""), sep= "\t", row.names = FALSE, quote= FALSE) 
  #prepare tables directly for upload on mitox
  resdata["dataset"]= dirname
  resdata["sample_ID"]= paste(tissue,"_",first, sep="")
  resdata["user_ID"] = "mitox"
  write.table(resdata[,c("user_ID","sample_ID","Gene",paste("Mean_",second, sep=""),paste("Mean_",first, sep=""),"log2FoldChange","pvalue")], file = paste("mitox_",dirname,"_.csv", sep=""), sep= ",", row.names = FALSE, quote= FALSE)
}

