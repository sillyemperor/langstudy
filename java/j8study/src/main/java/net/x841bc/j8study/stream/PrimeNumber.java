package net.x841bc.j8study.stream;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class PrimeNumber implements Iterable<Long>, Iterator<Long> {
	
	final static List<Long> PRIMES = Arrays.asList(2l, 3l, 5l, 7l, 9l);

	public static boolean check(long x) {
		if(x < 2) {
			return false;
		}
		if(PRIMES.contains(x)) {
			return true;
		}
		if(x % 2 == 0) {
			return false;
		}
		if(x % 3 == 0) {
			return false;
		}
		if(x % 5 == 0) {
			return false;
		}
		if(x % 7 == 0) {
			return false;
		}
		if(x % 9 == 0) {
			return false;
		}
		return true;
	}
	
	final static long NUM = 1000000000l;
	final static long HALF = NUM/2;
	
	public static void main(String[] args) throws InterruptedException, ExecutionException {
		long t = System.currentTimeMillis();
		
		long count = 0;
//		for(Long i:new PrimeNumber(NUM)) {
//			if(i != null) {
//				++count;
//			}
//		}
//		System.out.println(System.currentTimeMillis()-t);
//		System.out.println(count);
		//6776
		//228571432
		
		ExecutorService pool = Executors.newWorkStealingPool();
		
		t = System.currentTimeMillis();
		count = pool.invokeAll(Arrays.asList(new Callable<Long>() {

			@Override
			public Long call() throws Exception {
				long count = 0;
				for(Long i:new PrimeNumber(0, HALF)) {
					if(i != null) {
						++count;
					}
				}
				return count;				
			}
			
		},new Callable<Long>() {

			@Override
			public Long call() throws Exception {
				long count = 0;
				for(Long i:new PrimeNumber(HALF+1, NUM)) {
					if(i != null) {
						++count;
					}
				}
				return count;
			}
			
		})).stream().mapToLong(i -> {
			try {
				return i.get();
			} catch (InterruptedException | ExecutionException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			return 0l;
		}).reduce((a,b) -> a+b).getAsLong();
		
		System.out.println(System.currentTimeMillis()-t);
		System.out.println(count);
	}
	
	private long index;
	private long num;

	public PrimeNumber(long index, long num) {
		super();
		this.num = num;
		this.index = index;
	}
	
	public PrimeNumber(long num) {
		this(2, num);
	}

	@Override
	public Iterator<Long> iterator() {
		return this;
	}


	@Override
	public boolean hasNext() {
		return index < num;
	}

	@Override
	public Long next() {
		Long ret = null;
		for(;hasNext();++index) {
			if(check(index)) {
				ret = index;
				++index;
				break;
			}
		}
		return ret;
	}
}
