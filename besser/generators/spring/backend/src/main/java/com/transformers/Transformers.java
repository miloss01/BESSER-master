package com.transformers;

import com.transformers.entity.Computer;
import com.transformers.service.interfaces.IComputerService;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ApplicationContext;

import java.util.ArrayList;

@SpringBootApplication
public class Transformers {

	public static void main(String[] args) {
		ApplicationContext context = SpringApplication.run(Transformers.class, args);

		IComputerService computerService = context.getBean(IComputerService.class);

		// kreiranje racunara
		Computer c = new Computer();
		c.setModel("ThinkPad X1");

		// cuvanje
		computerService.save(c);

		System.out.println("Saved computer id: " + c.getId());

		// pretraga
		ArrayList<Computer> found = computerService.findAllByModel("ThinkPad X1");

		for (Computer computer : found) {
			System.out.println(computer.getId());
			System.out.println(computer.getModel());
		}
	}

}