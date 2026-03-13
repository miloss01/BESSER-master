package com.transformers.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "computers")
public class Computer extends Thing {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", nullable = false)
    public Integer id;
    
    @Column(name = "model", nullable = false)
    public String model;
    
    public Computer() { }

    public Computer(Integer id, String model) {
        this.id = id;
        this.model = model;
    }
    
    public Integer getId() {
        return this.id;
    }

    public void setId(Integer id) {
        this.id = id;
    }
    
    public String getModel() {
        return this.model;
    }

    public void setModel(String model) {
        this.model = model;
    }
    
}