package net.x841bc.j8study.crypt;

import java.io.UnsupportedEncodingException;
import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;

import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;

public class AESDemo2 {

	public static void main(String[] args)
			throws UnsupportedEncodingException, NoSuchAlgorithmException, NoSuchPaddingException, InvalidKeyException,
			InvalidAlgorithmParameterException, IllegalBlockSizeException, BadPaddingException {
		String data = "Hello";
		String key = "1234567890123456";
		String algoName = "AES";
		String transform = "AES/CBC/PKCS5Padding";
		final SecretKeySpec secKey = new SecretKeySpec("jhbvibi6g97y(&^Gbh JG KGVKj H J ".getBytes("UTF-8"), algoName);
		final IvParameterSpec iv = new IvParameterSpec("1234567890123456".getBytes("UTF-8"));

		Cipher cipher = Cipher.getInstance(transform);
		cipher.init(Cipher.ENCRYPT_MODE, secKey, iv);
		byte[] encodeData = cipher.doFinal(data.getBytes("UTF-8"));

		cipher.init(Cipher.DECRYPT_MODE, secKey, iv);
		byte[] decodeData = cipher.doFinal(encodeData);

		System.out.println(new String(decodeData, "UTF-8"));
	}

}
