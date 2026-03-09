package spring.entities;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

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