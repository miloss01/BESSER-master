package com.transformers.service.interfaces;

import com.transformers.entity.Role;
import com.transformers.entity.User;
import java.time.Duration;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

public interface IUserService {

        void delete(User user);
        List<User> findAll();
        ArrayList<User> findAllByAge(Integer age);
        ArrayList<User> findAllByBirthday(Duration birthday);
        ArrayList<User> findAllByBirthday2(LocalDateTime birthday2);
        ArrayList<User> findAllByBirthday2Between(LocalDateTime start, LocalDateTime end);
        ArrayList<User> findAllByEmail(String email);
        ArrayList<User> findAllByRole(Role role);
        Optional<User> findById(Integer id);
        User save(User user);
        
}