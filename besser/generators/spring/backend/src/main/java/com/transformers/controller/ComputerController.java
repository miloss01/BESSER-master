package com.transformers.controller;

import com.transformers.entity.Computer;
import com.transformers.service.interfaces.IComputerService;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/computer")
public class ComputerController {

    @Autowired
    private IComputerService _computerService;

    @GetMapping
    public ResponseEntity<List<Computer>> getAll() {
        return ResponseEntity.ok(_computerService.findAll());
    }

    @GetMapping("/{id}")
    public ResponseEntity<Computer> getById(@PathVariable Integer id) {
        return _computerService.findById(id).map(ResponseEntity::ok).orElseGet(() -> ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<Computer> create(@RequestBody Computer entity) {
        Computer saved = _computerService.save(entity);
        return ResponseEntity.ok(saved);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Computer> update(@PathVariable Integer id, @RequestBody Computer entity) {

        Optional<Computer> existing = _computerService.findById(id);

        if (existing.isEmpty()) {
            return ResponseEntity.notFound().build();
        }

        entity.setId(id);
        Computer updated = _computerService.save(entity);

        return ResponseEntity.ok(updated);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteById(@PathVariable Integer id) {

        Optional<Computer> existing = _computerService.findById(id);

        if (existing.isEmpty()) {
            return ResponseEntity.notFound().build();
        }

        _computerService.delete(existing.get());

        return ResponseEntity.noContent().build();
    }

}