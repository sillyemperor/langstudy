package net.x841bc.j8study.crypt;

import java.security.Key;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.NoSuchAlgorithmException;

import org.apache.commons.codec.binary.Base64;

public class RSADemo {

	public static void main(String[] args) throws NoSuchAlgorithmException {
		KeyPairGenerator kpg = KeyPairGenerator.getInstance("RSA");
		kpg.initialize(2048);
		KeyPair kp = kpg.genKeyPair();
		Key publicKey = kp.getPublic();
		Key privateKey = kp.getPrivate();
		System.out.println(Base64.encodeBase64String(privateKey.getEncoded()));
		System.out.println(Base64.encodeBase64String(publicKey.getEncoded()));
		
	}

}
