package com.transformers.repository;

import com.transformers.entity.Role;
import com.transformers.entity.User;
import java.time.Duration;
import java.time.LocalDateTime;
import java.util.ArrayList;
import org.springframework.data.jpa.repository.JpaRepository;

public interface IUserRepository extends JpaRepository<User, Integer> {

        ArrayList<User> findAllByAge(Integer age);
        ArrayList<User> findAllByBirthday(Duration birthday);
        ArrayList<User> findAllByBirthday2(LocalDateTime birthday2);
        ArrayList<User> findAllByBirthday2Between(LocalDateTime start, LocalDateTime end);
        ArrayList<User> findAllByEmail(String email);
        ArrayList<User> findAllByRole(Role role);
        
}