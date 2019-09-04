package net.x841bc.j8study.async;

import java.util.concurrent.CompletableFuture;

public class CompletableFutureDemo {

	public static void main(String[] args) {
		CompletableFuture.supplyAsync(() -> Thread.currentThread().getName() + " Hello").thenAccept(System.out::println);
		
	}

}
