package main

import (
	"fmt"
	"os"
)

var n int
var tree []int

func find(x int) int {
	if tree[x] == x {
		return x
	} else {
		tree[x] = find(x)
		return tree[x]
	}
}

func union(x, y int) {
	px := find(x)
	py := find(y)

	tree[px] = py
}

func main() {
	outfile, _ := os.Create("../test.out")
	defer outfile.Close()

	fmt.Scan(&n)
	tree = make([]int, n)
	for i := range tree {
		tree[i] = i
	}

	mat := make([][]float64, n)
	for i := range mat {
		mat[i] = make([]float64, n)
	}

	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			fmt.Scan(&mat[i][j])
		}
	}

	for rep := 0; rep < n-1; rep++ {
		mindist := 987654321.0
		minidxi := -1
		minidxj := -1

		for i := 0; i < n; i++ {
			for j := i + 1; j < n; j++ {
				if find(i) == find(j) {
					continue
				}

				if mindist > mat[i][j] {
					mindist = mat[i][j]
					minidxi = i
					minidxj = j
				}
			}
		}

		union(minidxi, minidxj)
	}

	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			fmt.Printf("%.2f ", mat[i][j])
		}
		fmt.Printf("\n")
	}
}
