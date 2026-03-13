package com.transformers.service.interfaces;

import com.transformers.entity.Computer;
import java.util.ArrayList;
import java.util.Optional;

public interface IComputerService {

        void delete(Computer computer);
        ArrayList<Computer> findAllByModel(String model);
        Optional<Computer> findById(Integer id);
        Computer save(Computer computer);
        
}