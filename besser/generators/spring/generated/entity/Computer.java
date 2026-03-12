package spring.entities;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity
@Table(name = "computers")
public class Computer extends Thing {
    
    @ManyToMany
    @JoinTable(name = "many_to_many",
        joinColumns = @JoinColumn(name = "computer_id"),
        inverseJoinColumns = @JoinColumn(name = "user_id"))
    private List<User> owners = new ArrayList<>();
    
    public Computer() { }

    
    
}