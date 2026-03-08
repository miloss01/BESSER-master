package spring.entities;

import jakarta.persistence.Entity;
import jakarta.persistence.Table;
import jakarta.persistence.Id;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Column;
import jakarta.persistence.Enumerated;
import java.time.Duration;

@Entity
@Table(name="users")
public class User {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "email")
    public String email;
    
    @Enumerated(EnumType.STRING)
    public Hand hand;
    
    @Enumerated(EnumType.STRING)
    private Role role;
    
    @Column(name = "age", nullable = false)
    public Integer age = 2;
    
    @Column(name = "birthday", nullable = false)
    protected Duration birthday;
    
    @Column(name = "first_name")
    public String firstName = "John";
    
    public User() { }

    public User(String email, Hand hand, Role role, Integer age, Duration birthday, String firstName) {
        this.email = email;
        this.hand = hand;
        this.role = role;
        this.age = age;
        this.birthday = birthday;
        this.firstName = firstName;
    }
    
    public String getEmail() {
        return this.email;
    }

    public void setEmail(String email) {
        this.email = email;
    }
    
    public Hand getHand() {
        return this.hand;
    }

    public void setHand(Hand hand) {
        this.hand = hand;
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
    
    public String getFirstname() {
        return this.firstName;
    }

    public void setFirstname(String firstName) {
        this.firstName = firstName;
    }
    
}