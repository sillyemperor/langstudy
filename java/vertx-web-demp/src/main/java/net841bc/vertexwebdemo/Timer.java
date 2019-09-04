package net841bc.vertexwebdemo;

import io.vertx.core.Vertx;

public class Timer {

	public static void main(String[] args) {
		
		Vertx vertx = Vertx.vertx();
		
		System.out.println("Main "+Thread.currentThread().getName());
		vertx.setPeriodic(100, id -> {
			System.out.println("Timer1 "+Thread.currentThread().getName());
			System.out.print("\b");
			
			try {
				Thread.sleep(1000);
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		});
		vertx.setPeriodic(100, id -> {
			System.out.println("Timer2 "+Thread.currentThread().getName());
			System.out.print("\b");
		});
	}

}
