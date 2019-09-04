package net.x841bc.j8study.crypt;

import java.io.UnsupportedEncodingException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;

import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.KeyGenerator;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;

import org.apache.commons.codec.DecoderException;
import org.apache.commons.codec.binary.Hex;

public class AESDemo1 {

	public static void main(String[] args) throws NoSuchAlgorithmException, NoSuchPaddingException, InvalidKeyException, IllegalBlockSizeException, BadPaddingException, UnsupportedEncodingException, DecoderException {
		String data = "Hello";
		
		KeyGenerator keygenerator = KeyGenerator.getInstance("AES");
		keygenerator.init(256);
//		SecretKey scrKey = keygenerator.generateKey();
//		System.out.println(Hex.encodeHex(scrKey.getEncoded()));
	    SecretKey scrKey = new SecretKeySpec(Hex.decodeHex("2602c1fa1a237c2b264a2f18cb213fb1e041879374a831be695ea589e56be667"), "AES");
	    
	    
	    Cipher cipher = Cipher.getInstance("AES");
	    cipher.init(Cipher.ENCRYPT_MODE, scrKey);	    
	    byte[] encodeData = cipher.doFinal(data.getBytes("UTF-8"));
	    
	    cipher.init(Cipher.DECRYPT_MODE, scrKey);	    
	    byte[] decodeData = cipher.doFinal(encodeData);
	    
	    System.out.println(new String(decodeData, "UTF-8"));
	}

}
