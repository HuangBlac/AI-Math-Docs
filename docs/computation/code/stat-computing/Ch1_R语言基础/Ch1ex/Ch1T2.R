# 请从本脚本所在目录运行；示例数据与脚本放在同一目录。
getwd()
data = read.csv("2015city.csv", fileEncoding = "GBK", header = TRUE)
city_col = "城市"
colnames(data)
cost_cols =setdiff(colnames(data),city_col)

for (cost_col in cost_cols){
  single_data = data.frame(
    城市 = data[[city_col]],
    费用 = data[[cost_col]]
  )
  
  outfile = paste0(cost_col, ".csv")
  
  write.csv(
    x=single_data, 
    file = outfile, 
    fileEncoding = "GBK", 
    row.names = FALSE 
  )
}

getwd()  
