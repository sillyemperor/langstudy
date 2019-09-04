package net.x841bc.j8study.util;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class ListGenerations {
	
	public static List<Integer> randomInt(int n) {
		List<Integer> ret = new ArrayList<Integer>(n);
		Random rand = new Random(n);
		for(;n>=0; --n) {
			ret.add(rand.nextInt());
		}
		return ret;
	}

}
