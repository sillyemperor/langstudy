package net841bc;

import java.awt.Font;
import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.List;

import javax.imageio.ImageIO;
import javax.servlet.http.HttpServletResponse;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.http.HttpEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import reactor.core.publisher.Mono;


@SpringBootApplication
@RestController
@Api(tags="Main")
public class WebApplication {

	@GetMapping("/")
	@ApiOperation(value = "问候")
	public String hello() throws InterruptedException {
		return Thread.currentThread().getName()+" Hello";
	}
	
	@GetMapping("/flux")
	public Mono<String> helloFlux() throws InterruptedException {
		return Mono.just(Thread.currentThread().getName()+" Hello");//.delayElement(Duration.ofSeconds(1));
	}
	
	@GetMapping("/watermark")
	public void watermark(HttpServletResponse response) throws IOException {
		BufferedImage image = ImageIO.read(new File("a.jpg"));
		
		Graphics2D g = image.createGraphics();
		g.setFont(Font.decode("宋体"));
		g.drawString("你好", 100, 100);
		g.dispose();
		
		response.setHeader("content-type", "image/jpeg");
		ImageIO.write(image, "JPEG", response.getOutputStream());
		
	}
	
	@Autowired
	private CustomerRepository customer;
	
	@GetMapping("/customer/{id}")
	public HttpEntity<Customer> getCustomer(@PathVariable long id) {
		return new HttpEntity<Customer>(customer.findById(id).orElse(null));
	}
	
	@GetMapping("/customer")
	public HttpEntity<List<Customer>> queryCustomer(@RequestParam String lastName) {
		return new HttpEntity<List<Customer>>(customer.findByLastName(lastName));
	}
	
	@PostMapping("/customer")
	public HttpEntity<Customer> addCustomer(@RequestBody Customer ett) {
		return new HttpEntity<Customer>(customer.save(ett));
	}

	public static void main(String[] args) {
		SpringApplication.run(WebApplication.class, args);
	}

}
