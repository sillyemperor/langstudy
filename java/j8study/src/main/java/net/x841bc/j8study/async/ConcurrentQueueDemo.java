package net.x841bc.j8study.async;

import java.util.concurrent.BlockingQueue;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.TimeUnit;

public class ConcurrentQueueDemo {

	public static void main(String[] args) throws InterruptedException {
		
		System.out.println("No blocking");
		noBlocking();
		
		System.out.println("Blocking");
		blocking();
	}

	private static void blocking() throws InterruptedException {
//		final BlockingQueue<String> queue = new ArrayBlockingQueue<String>(1000);
		final BlockingQueue<String> queue = new LinkedBlockingQueue<String>();
				
		Thread produce = new Thread(() -> {
			
//			System.out.println("Start A");
			for(int i = 0;i<10;++i) {
				queue.offer("A"+i);
			}
			
			try {
//				System.out.println("Wait");
				Thread.sleep(1000);
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			
//			System.out.println("Start B");
			for(int i = 0;i<10;++i) {
				queue.offer("B"+i);
			}
//			System.out.println("End");
		});
		
		Thread consumer = new Thread(() -> {
			String q = null;
			try {
				while((q = queue.poll(2, TimeUnit.SECONDS)) != null) {
					System.out.println(q);
				}
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		});
		
		produce.start();
		consumer.start();
		
		consumer.join();
		produce.join();
		
	}

	private static void noBlocking() throws InterruptedException {
		final ConcurrentLinkedQueue<String> queue = new ConcurrentLinkedQueue<String>();
				
		Thread produce = new Thread(() -> {
			
			for(int i = 0;i<10;++i) {
				queue.add("A"+i);
			}
			
			try {
				Thread.sleep(1000);
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			
			for(int i = 0;i<10;++i) {
				queue.add("B"+i);
			}
		});
		
		Thread consumer = new Thread(() -> {
			String q = null;
			while((q = queue.poll()) != null) {
				System.out.println(q);				
			}
		});
		
		produce.start();
		consumer.start();
		
		produce.join();
		consumer.join();
	}

}
