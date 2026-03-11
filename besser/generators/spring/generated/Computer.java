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
    
    @OneToOne
    @JoinColumn(name = "user_id")
    private User owner;
    
    @ManyToOne
    @JoinColumn(name = "user_id")
    private User ownerr;
    
    public Computer() { }

    
    
}