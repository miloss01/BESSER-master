package spring.entities;

import jakarta.persistence.Entity;
import jakarta.persistence.Table;
import jakarta.persistence.Id;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Column;

@Entity
@Table(name="computers")
public class Computer extends Thing {
    
    @Column(name = "name", nullable = false)
    public String name;
    
    public Computer() { }

    public Computer(String name) {
        this.name = name;
    }
    
    public String getName() {
        return this.name;
    }

    public void setName(String name) {
        this.name = name;
    }
    
}