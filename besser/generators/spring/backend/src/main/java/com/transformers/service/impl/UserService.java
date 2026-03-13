package com.transformers.service.impl;

import com.transformers.entity.Role;
import com.transformers.entity.User;
import com.transformers.repository.IUserRepository;
import com.transformers.service.interfaces.IUserService;
import java.time.Duration;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class UserService implements IUserService {

    @Autowired
    private IUserRepository _userRepository;

    @Override
    public void delete(User user) {
        _userRepository.delete(user);
    }
    
    @Override
    public ArrayList<User> findAllByAge(Integer age) {
        return _userRepository.findAllByAge(age);
    }
    
    @Override
    public ArrayList<User> findAllByBirthday(Duration birthday) {
        return _userRepository.findAllByBirthday(birthday);
    }
    
    @Override
    public ArrayList<User> findAllByBirthday2(LocalDateTime birthday2) {
        return _userRepository.findAllByBirthday2(birthday2);
    }
    
    @Override
    public ArrayList<User> findAllByBirthday2Between(LocalDateTime start, LocalDateTime end) {
        return _userRepository.findAllByBirthday2Between(start, end);
    }
    
    @Override
    public ArrayList<User> findAllByEmail(String email) {
        return _userRepository.findAllByEmail(email);
    }
    
    @Override
    public ArrayList<User> findAllByRole(Role role) {
        return _userRepository.findAllByRole(role);
    }
    
    @Override
    public Optional<User> findById(Integer id) {
        return _userRepository.findById(id);
    }
    
    @Override
    public User save(User user) {
        return _userRepository.save(user);
    }
    
    
}