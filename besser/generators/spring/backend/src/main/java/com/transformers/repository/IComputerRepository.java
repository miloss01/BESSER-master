package com.transformers.repository;

import com.transformers.entity.Computer;
import java.util.ArrayList;
import org.springframework.data.jpa.repository.JpaRepository;

public interface IComputerRepository extends JpaRepository<Computer, Integer> {

        ArrayList<Computer> findAllByModel(String model);
        
}