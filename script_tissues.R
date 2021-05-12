if (!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager")
BiocManager::install("DESeq2")
# file with the pseudo replicates 
library(readxl)
matrix = data.frame(read_excel(file.choose()), row.names = 1) #select the mean file
dim(matrix)

coldata =  data.frame(read_excel(file.choose()), row.names = 1) #select the matrix file 
#create deseq object
library("DESeq2")
dds <- DESeqDataSetFromMatrix(countData=matrix, colData=coldata, design= ~tissues)
#get the time point
age = strsplit(colnames(matrix)[1],'_')[[1]][2]
#run deseq2

dds <- DESeq(dds)
dds
#pairwise comparaisons 
library("operator.tools")
comparisons<- c('BAT_VS_mean','Bone_VS_mean','Brain_VS_mean','GAT_VS_mean','Heart_VS_mean','Kidney_VS_mean','LimbMuscle_VS_mean','Liver_VS_mean','Lung_VS_mean','Marrow_VS_mean','MAT_VS_mean','Pancreas_VS_mean','SCAT_VS_mean','Skin_VS_mean','SmallIntestine_VS_mean','Spleen_VS_mean','WBC_VS_mean')
columns = colnames(matrix)



dir <- "/home/kaouther/Documents/Internship/"


FDRthreshold<-0.05


for (dirname in comparisons){
  tissue = strsplit(dirname,'_')[[1]][1]
  dir.create(paste(dir, dirname, sep=""))
  #set working directory
  setwd(paste(dir,dirname, sep=""))
  #choose the contrast
  first <- strsplit(dirname, "_VS_")[[1]][1]
  second <- strsplit(dirname, "_VS_")[[1]][2]
  res <- results(dds,c('tissues',first, second))
  
  
  ## Order by adjusted p-value
  res <- res[order(res$padj), ]
  
  ## Merge with normalized count data
  resdata <- merge(as.data.frame(res), as.data.frame(counts(dds, normalized=TRUE)), by="row.names", sort=FALSE)
  #compute the mean for condition
  resdata[paste("Mean_",second, sep="")]<-rowMeans(resdata[,as.character(coldata[coldata$tissues==second, "Name"])])
  resdata[paste("Mean_", first,sep="")]<-rowMeans(resdata[,as.character(coldata[coldata$tissues==first, "Name"])])
  colnames(resdata)[1]<-"Gene"
  write.table(resdata, file = paste("complete-results_",dim(resdata)[1],"_.txt", sep=""), sep= "\t", row.names = FALSE, quote= FALSE) 
  #prepare tables directly for upload on mitox
  resdata["dataset"]= dirname
  resdata["sample_ID"]= paste(tissue,"_",age, sep="")
  resdata["user_ID"] = "mitox"
  write.table(resdata[,c("user_ID","sample_ID","Gene",paste("Mean_",second, sep=""),paste("Mean_",first, sep=""),"log2FoldChange","pvalue")], file = paste("mitox_",paste(tissue,"_",age, sep=""),"_.csv", sep=""), sep= ",", row.names = FALSE, quote= FALSE)
}
