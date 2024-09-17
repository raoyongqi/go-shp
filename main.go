package main

import (
	"fmt"
	"log"
	"strconv"

	"github.com/jonas-p/go-shp"
)

func main() {
	// 打开 shapefile 文件
	file, err := shp.Open("C:/Users/r/Desktop/china/shp/vegetation_china.shp")
	if err != nil {
		log.Fatalf("打开文件时出错: %v", err)
	}
	defer file.Close()

	// 获取文件的总记录数
	fmt.Printf("总记录数: %d\n", file.AttributeCount())
	// 获取文件的边界框
	bbox := file.BBox()
	fmt.Printf("边界框: Xmin: %f, Ymin: %f, Xmax: %f, Ymax: %f\n", bbox.MinX, bbox.MinY, bbox.MaxX, bbox.MaxY)
	fields := file.Fields()
	// 设置计数器，限制输出前 10 条记录
	count := 0
	maxRecords := 10
	// loop through all features in the shapefile
	for file.Next() {
		// 获取当前几何形状和索引
		n, p := file.Shape()

		// 打印几何形状的边界框
		fmt.Println("边界框:", p.BBox())

		// 打印属性
		for k, f := range fields {
			val := file.ReadAttribute(n, k)
			if f.String() == "植被_4" {
				fmt.Printf("\t%v: %v\n", f, val)
			}

		}

		fmt.Println()

		// 增加计数器
		count++

		// 如果已打印了 10 条记录，退出循环
		if count >= maxRecords {
			break
		}
	}
	points := []shp.Point{
		{X: 10.0, Y: 10.0},
		{X: 10.0, Y: 15.0},
		{X: 15.0, Y: 15.0},
		{X: 15.0, Y: 10.0},
	}

	// fields to write
	fields = []shp.Field{
		// String attribute field with length 25
		shp.StringField("NAME", 25),
	}

	// create and open a shapefile for writing points
	shpFile, err := shp.Create("shp/points/points.shp", shp.POINT)
	if err != nil {
		log.Fatal(err)
	}
	defer shpFile.Close()

	// setup fields for attributes
	shpFile.SetFields(fields)

	// write points and attributes
	for n, point := range points {
		shpFile.Write(&point)

		// write attribute for object n for field 0 (NAME)
		shpFile.WriteAttribute(n, 0, "Point "+strconv.Itoa(n+1))
	}

	log.Println("Shapefile created successfully")
}
