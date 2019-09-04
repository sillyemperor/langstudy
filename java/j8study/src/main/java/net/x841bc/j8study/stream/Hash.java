package net.x841bc.j8study.stream;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.util.stream.IntStream;

import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.spec.SecretKeySpec;

import org.apache.commons.io.IOUtils;

public class Hash {

	public static void main(String[] args) throws NoSuchAlgorithmException, NoSuchPaddingException, FileNotFoundException, IOException, InvalidKeyException {
		String s = IOUtils.toString(new FileInputStream("hp7.txt"));
		byte[] data = s.getBytes();
		int n = 1000;
		
		{
			long t = System.currentTimeMillis();
			IntStream.range(0, n).forEach(i -> {
				try {
					Cipher aes = Cipher.getInstance("AES");
					final SecretKeySpec key = new SecretKeySpec("123456789qwertyu".getBytes(StandardCharsets.UTF_8), "AES");
					aes.init(Cipher.ENCRYPT_MODE, key);		
					aes.update(data);				
					aes.doFinal();
				} catch (IllegalBlockSizeException | BadPaddingException | InvalidKeyException | NoSuchAlgorithmException | NoSuchPaddingException e) {
					e.printStackTrace();
				}
			});
			System.out.println(System.currentTimeMillis() - t);
		}
		
		{	
			long t = System.currentTimeMillis();
			IntStream.range(0, n).parallel().forEach(i -> {
				try {
					Cipher aes = Cipher.getInstance("AES");
					final SecretKeySpec key = new SecretKeySpec("123456789qwertyu".getBytes(StandardCharsets.UTF_8), "AES");
					aes.init(Cipher.ENCRYPT_MODE, key);		
					aes.update(data);				
					aes.doFinal();
				} catch (IllegalBlockSizeException | BadPaddingException | InvalidKeyException | NoSuchAlgorithmException | NoSuchPaddingException e) {
					e.printStackTrace();
				}
			});
			System.out.println(System.currentTimeMillis() - t);
		}
	}

}
