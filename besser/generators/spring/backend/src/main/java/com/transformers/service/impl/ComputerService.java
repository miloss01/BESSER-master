package com.transformers.service.impl;

import com.transformers.entity.Computer;
import com.transformers.repository.IComputerRepository;
import com.transformers.service.interfaces.IComputerService;
import java.util.ArrayList;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class ComputerService implements IComputerService {

    @Autowired
    private IComputerRepository _computerRepository;

    @Override
    public void delete(Computer computer) {
        _computerRepository.delete(computer);
    }
    
    @Override
    public ArrayList<Computer> findAllByModel(String model) {
        return _computerRepository.findAllByModel(model);
    }
    
    @Override
    public Optional<Computer> findById(Integer id) {
        return _computerRepository.findById(id);
    }
    
    @Override
    public Computer save(Computer computer) {
        return _computerRepository.save(computer);
    }
    
    
}