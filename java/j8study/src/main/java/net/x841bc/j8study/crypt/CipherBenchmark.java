package net.x841bc.j8study.crypt;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.security.GeneralSecurityException;
import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.Key;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.util.Properties;

import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.KeyGenerator;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.SecretKey;
import javax.crypto.ShortBufferException;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;

import org.apache.commons.crypto.cipher.CryptoCipher;
import org.apache.commons.crypto.cipher.CryptoCipherFactory;
import org.apache.commons.crypto.cipher.CryptoCipherFactory.CipherProvider;
import org.apache.commons.crypto.utils.Utils;

public class CipherBenchmark {

	public static void main(String[] args) throws GeneralSecurityException, Exception {
		String key = "1234567890123456";
		String data = "看别人不顺眼，是自己修养不够。!";
		
		int n = 10000;
		executeAes(key, data, n);
		executeDes(key, data, n);
		executeRsa(data, n);
	}
	
	private static void executeRsa(String data, int n) throws NoSuchAlgorithmException, NoSuchPaddingException, InvalidKeyException, IllegalBlockSizeException, BadPaddingException, UnsupportedEncodingException {
		KeyPairGenerator kpg = KeyPairGenerator.getInstance("RSA");
		kpg.initialize(2048);
		KeyPair kp = kpg.genKeyPair();
		Key publicKey = kp.getPublic();
		Key privateKey = kp.getPrivate();
		Cipher desCipher = Cipher.getInstance("RSA");
		desCipher.init(Cipher.ENCRYPT_MODE, publicKey);
		
		byte[] textEncrypted = null;
		long encodeTime = System.currentTimeMillis();
		for(int i=0;i<n;++i) {
			textEncrypted = desCipher.doFinal(data.getBytes("UTF-8"));
		}
		encodeTime = System.currentTimeMillis() - encodeTime;
		
		desCipher.init(Cipher.DECRYPT_MODE, privateKey);
		long decodeTime = System.currentTimeMillis();
		for(int i=0;i<n;++i) {	    
			desCipher.doFinal(textEncrypted);
			
		}
		decodeTime = System.currentTimeMillis() - decodeTime;
		
		System.out.println("RSA "+encodeTime+" "+decodeTime);
	}

	private static void executeDes(String key, String data, int n) throws NoSuchAlgorithmException, NoSuchPaddingException, InvalidKeyException, IllegalBlockSizeException, BadPaddingException, IOException {
		KeyGenerator keygenerator = KeyGenerator.getInstance("DES");
		keygenerator.init(new SecureRandom(key.getBytes()));
	    SecretKey myDesKey = keygenerator.generateKey();
	    System.out.println(myDesKey.getEncoded().length);
	    Cipher desCipher = Cipher.getInstance("DES/ECB/PKCS5Padding");
	    desCipher.init(Cipher.ENCRYPT_MODE, myDesKey);
	    
	    byte[] textEncrypted = null;
	    long encodeTime = System.currentTimeMillis();	    
	    for(int i=0;i<n;++i) {
	    		textEncrypted = desCipher.doFinal(data.getBytes("UTF-8"));
	    }
	    encodeTime = System.currentTimeMillis() - encodeTime;
	    
	    desCipher.init(Cipher.DECRYPT_MODE, myDesKey);
	    long decodeTime = System.currentTimeMillis();	    
	    for(int i=0;i<n;++i) {
	    		desCipher.doFinal(textEncrypted);
	    		
	    }
	    decodeTime = System.currentTimeMillis() - decodeTime;
	    System.out.println("DES "+encodeTime+" "+decodeTime);
	}

	private static void executeAes(String key, String data, int n)
			throws UnsupportedEncodingException, IOException, InvalidKeyException, InvalidAlgorithmParameterException,
			ShortBufferException, IllegalBlockSizeException, BadPaddingException {
		String algoName = "AES";
		String transform = "AES/CBC/PKCS5Padding";
		final SecretKeySpec secKey = new SecretKeySpec(key.getBytes("UTF-8"), algoName);
		final IvParameterSpec iv = new IvParameterSpec(key.getBytes("UTF-8"));
		System.out.println(secKey.getEncoded().length);
		
		Properties properties = new Properties();
		properties.setProperty(CryptoCipherFactory.CLASSES_KEY, CipherProvider.OPENSSL.getClassName());		
		
		CryptoCipher encipher = Utils.getCipherInstance(transform, properties);
		
		byte[] input = data.getBytes("UTF-8");
		byte[] output = new byte[64];
		
		int updateBytes = 0;
		encipher.init(Cipher.ENCRYPT_MODE, secKey, iv);
		long encodeTime = System.currentTimeMillis();	    
	    for(int i=0;i<n;++i) {
	    		updateBytes = encipher.update(input, 0, input.length, output, 0);		
	    		updateBytes += encipher.doFinal(input, 0, 0, output, updateBytes);
	    }
	    encodeTime = System.currentTimeMillis() - encodeTime;
		encipher.close();
				
		properties.setProperty(CryptoCipherFactory.CLASSES_KEY, CipherProvider.JCE.getClassName());
		CryptoCipher decipher = Utils.getCipherInstance(transform, properties);
		
		decipher.init(Cipher.DECRYPT_MODE, secKey, iv);
		byte [] decoded = new byte[64];
		long decodeTime = System.currentTimeMillis();	    
	    for(int i=0;i<n;++i) {
	    		decipher.doFinal(output, 0, updateBytes, decoded, 0);
//	    		System.out.println(new String(decoded, "utf-8"));
	    }
	    decodeTime = System.currentTimeMillis() - decodeTime;
	    System.out.println("AES "+encodeTime+" "+decodeTime);
	}

}
