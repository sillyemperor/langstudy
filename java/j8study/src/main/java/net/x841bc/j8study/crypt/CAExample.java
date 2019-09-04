package net.x841bc.j8study.crypt;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.net.URL;
import java.security.cert.CertificateFactory;
import org.apache.commons.io.IOUtils;

import java.security.cert.Certificate;
import java.security.cert.CertificateException;

public class CAExample {

	public static void main(String[] args) throws CertificateException, IOException {
		URL rootCaFile = CAExample.class.getClassLoader().getResource("root.crt");
		URL clientCaFile = CAExample.class.getClassLoader().getResource("client.crt");
		URL client1CaFile = CAExample.class.getClassLoader().getResource("client1.crt");
		
	    final CertificateFactory certFactory = CertificateFactory.getInstance("X.509");
	    Certificate rootCA = certFactory.generateCertificates(
       		 new ByteArrayInputStream(IOUtils.toByteArray(rootCaFile))).iterator().next();
	    Certificate clientCA = certFactory.generateCertificates(
	       		 new ByteArrayInputStream(IOUtils.toByteArray(clientCaFile))).iterator().next();
	    Certificate client1CA = certFactory.generateCertificates(
	       		 new ByteArrayInputStream(IOUtils.toByteArray(client1CaFile))).iterator().next();
	    
	    System.out.println("--------Root CA----------");
	    System.out.println(rootCA.toString());
	    
	    System.out.println("--------Client CA----------");
//	    System.out.println(clientCA.toString());
	    verify(rootCA, clientCA);
	    
	    System.out.println("--------Client1 CA----------");
//	    System.out.println(client1CA.toString());	    
	    verify(rootCA, client1CA);
	}

	private static void verify(Certificate rootCA, Certificate clientCA) {
		try {
	    		clientCA.verify(rootCA.getPublicKey());
	    		System.out.println("验证成功");
	    } catch (Exception e) {
	    		System.out.println("验证失败："+e.getMessage());
	    }
	}

}
