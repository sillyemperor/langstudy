package net.x841bc.j8study.asm;

import static org.objectweb.asm.Opcodes.*;

import java.util.Arrays;

import org.objectweb.asm.ClassWriter;

public class GenerateClass extends ClassLoader {

	@Override
	protected Class<?> findClass(String name) throws ClassNotFoundException {
		if (name.equals("net.x841bc.j8study.asm.Comparable")) {
			ClassWriter cw = new ClassWriter(0);
			cw.visit(V1_5, ACC_PUBLIC + ACC_ABSTRACT + ACC_INTERFACE, "net/x841bc/j8study/asm/Comparable", null, "java/lang/Object",
					new String[] { "net/x841bc/j8study/asm/Mesurable" });
			cw.visitField(ACC_PUBLIC + ACC_FINAL + ACC_STATIC, "LESS", "I", null, new Integer(-1)).visitEnd();
			cw.visitField(ACC_PUBLIC + ACC_FINAL + ACC_STATIC, "EQUAL", "I", null, new Integer(0)).visitEnd();
			cw.visitField(ACC_PUBLIC + ACC_FINAL + ACC_STATIC, "GREATER", "I", null, new Integer(1)).visitEnd();
			cw.visitMethod(ACC_PUBLIC + ACC_ABSTRACT, "compareTo", "(Ljava/lang/Object;)I", null, null).visitEnd();
			cw.visitEnd();
			byte[] b = cw.toByteArray();
			return defineClass(name, b, 0, b.length);
		}
		return super.findClass(name);
	}

	public static void main(String[] args) throws ClassNotFoundException {
		ClassLoader clzLoader = new GenerateClass();
		
		Class<?> clz = clzLoader.loadClass("net.x841bc.j8study.asm.Comparable");
		
		System.out.println(clz);
		System.out.println(Arrays.toString(clz.getFields()));
		System.out.println(Arrays.toString(clz.getMethods()));
	}
}
