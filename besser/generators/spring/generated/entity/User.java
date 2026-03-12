package spring.entities;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.EnumType;
import javax.persistence.Enumerated;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity
@Table(name = "users")
public class User {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "email")
    public String email;
    
    @Enumerated(EnumType.STRING)
    private Role role;
    
    @Column(name = "first_name")
    public String firstName = "John";
    
    @ManyToMany(mappedBy = "owners")
    
    private List<Computer> computers = new ArrayList<>();
    
    public User() { }

    public User(String email, Role role, String firstName) {
        this.email = email;
        this.role = role;
        this.firstName = firstName;
    }
    
    public String getEmail() {
        return this.email;
    }

    public void setEmail(String email) {
        this.email = email;
    }
    
    public Role getRole() {
        return this.role;
    }

    public void setRole(Role role) {
        this.role = role;
    }
    
    public String getFirstname() {
        return this.firstName;
    }

    public void setFirstname(String firstName) {
        this.firstName = firstName;
    }
    
}