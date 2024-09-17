package main

import (
	"fmt"
	"log"
	"os"

	"github.com/LindsayBradford/go-dbf/godbf"
)

// Process 处理 .dbf 文件
func main() {
	inputDBF := "C:/Users/r/Desktop/china/shp/vegetation_china.dbf"

	// 打开 GBK 编码的 .dbf 文件
	file, err := os.Open(inputDBF)
	if err != nil {
		log.Fatalf("打开文件时出错: %v", err)
	}
	defer file.Close()
	fmt.Println(file)
	// 读取 .dbf 文件
	dbfTable, err := godbf.NewFromFile(inputDBF, "GBK")
	if err != nil {
		log.Fatalf("读取dbf: %v", err)
	}

	// 处理 DBF 表
	fmt.Println(dbfTable.NumberOfRecords())

}
