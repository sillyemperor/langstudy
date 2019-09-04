package net.x841bc.j8study.stream;

import java.util.List;
import java.util.stream.Collectors;

import net.x841bc.j8study.util.ListGenerations;

public class SortLargeList {

	public static void main(String[] args) {
		int n = 10;
		List<Integer> list = ListGenerations.randomInt(n);
		System.out.println(list);
		
		long t = System.currentTimeMillis();
		list.sort((a, b) -> {
			return a.compareTo(b);
		});
		System.out.println(list);
		System.out.println(System.currentTimeMillis() - t);
		
		t = System.currentTimeMillis();
		list = list.parallelStream().sorted((a, b) -> {
			return a.compareTo(b);
		}).collect(Collectors.toList());
		System.out.println(list);
		System.out.println(System.currentTimeMillis() - t);
	}

}
