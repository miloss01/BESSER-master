package com.transformers.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.JoinTable;
import jakarta.persistence.ManyToMany;
import jakarta.persistence.Table;
import java.time.Duration;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

@Entity
@Table(name = "users")
public class User {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", nullable = false)
    public Integer id;
    
    @Enumerated(EnumType.STRING)
    private Role role;
    
    @Column(name = "age", nullable = false)
    public Integer age = 2;
    
    @Column(name = "birthday", nullable = false)
    protected Duration birthday;
    
    @Column(name = "birthday2", nullable = false)
    protected LocalDateTime birthday2;
    
    @Column(name = "email")
    public String email;
    
    @ManyToMany
    @JoinTable(name = "many_to_many",
        joinColumns = @JoinColumn(name = "user_id"),
        inverseJoinColumns = @JoinColumn(name = "computer_id"))
    private List<Computer> computers = new ArrayList<>();
    
    public User() { }

    public User(Integer id, Role role, Integer age, Duration birthday, LocalDateTime birthday2, String email) {
        this.id = id;
        this.role = role;
        this.age = age;
        this.birthday = birthday;
        this.birthday2 = birthday2;
        this.email = email;
    }
    
    public Integer getId() {
        return this.id;
    }

    public void setId(Integer id) {
        this.id = id;
    }
    
    public Role getRole() {
        return this.role;
    }

    public void setRole(Role role) {
        this.role = role;
    }
    
    public Integer getAge() {
        return this.age;
    }

    public void setAge(Integer age) {
        this.age = age;
    }
    
    public Duration getBirthday() {
        return this.birthday;
    }

    public void setBirthday(Duration birthday) {
        this.birthday = birthday;
    }
    
    public LocalDateTime getBirthday2() {
        return this.birthday2;
    }

    public void setBirthday2(LocalDateTime birthday2) {
        this.birthday2 = birthday2;
    }
    
    public String getEmail() {
        return this.email;
    }

    public void setEmail(String email) {
        this.email = email;
    }
    
}