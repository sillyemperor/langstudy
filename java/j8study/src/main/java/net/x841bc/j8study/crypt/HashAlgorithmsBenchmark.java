package net.x841bc.j8study.crypt;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

import org.apache.commons.codec.digest.DigestUtils;

public class HashAlgorithmsBenchmark {

	public static void main(String[] args) throws NoSuchAlgorithmException {
		String data = "看别人不顺眼，是自己修养不够。!";
		
		byte[] md5Hash = DigestUtils.md5(data);
		System.out.println("MD5 bits "+md5Hash.length*8);
		
		byte[] sha1hash = DigestUtils.sha1(data);
		System.out.println("SHA-1 bits "+sha1hash.length*8);
		
		byte[] sha256hash = DigestUtils.sha256(data);
		System.out.println("SHA-256 bits "+sha256hash.length*8);
		
		int n = 10000;
		time(MessageDigest.getInstance("MD2"), n, data);
		time(MessageDigest.getInstance("SHA-1"), n, data);
		time(MessageDigest.getInstance("SHA-256"), n, data);
	}
	
	public static void time(MessageDigest alg, int n, String data) {
		DigestUtils diget = new DigestUtils(alg);
		
		long t = System.currentTimeMillis();		
		for(int i=0;i<n;++i) {
			diget.digest(data);
		}		
		System.out.println(alg.toString()+" use "+(System.currentTimeMillis()-t));
	}

}
